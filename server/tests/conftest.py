from pathlib import Path
from subprocess import check_call
from time import sleep, time

from httpx import AsyncClient, get, NetworkError
from pytest import fixture


def wait_until_responsive(url: str, timeout: float = 3.0) -> None:
    ref = time()
    now = ref
    while (now - ref) < timeout:
        try:
            response = get(url, verify=False)
            if response.status_code == 200:
                return
        except NetworkError:
            pass
        sleep(0.1)
        now = time()
    raise TimeoutError()


@fixture(scope='session')
def docker_compose() -> None:
    filename = Path(__file__).parent.parent / 'docker-compose.yml'
    docker_compose_up = f'docker-compose -f {filename} up -d'
    check_call(docker_compose_up, shell=True)
    try:
        wait_until_responsive('https://localhost')
        wait_until_responsive('https://localhost/fastapi_api/hello')
        wait_until_responsive('https://localhost/quart_api/hello')
        wait_until_responsive('https://localhost/tornado_api/hello')
        yield
    finally:
        check_call(['docker-compose', 'down'])


@fixture
async def client(docker_compose: None) -> AsyncClient:
    async with AsyncClient(base_url='https://localhost', verify=False, http2=True) as client:
        yield client
