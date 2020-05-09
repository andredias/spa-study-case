from pathlib import Path
from subprocess import check_call
from time import sleep, time

from httpx import AsyncClient, get, NetworkError
from pytest import fixture


def wait_until_responsive(timeout: float = 3.0) -> None:
    ref = time()
    now = ref
    while (now - ref) < timeout:
        try:
            response = get('https://localhost/api/hello', verify=False)
            if response.status_code == 200:
                return
        except NetworkError:
            pass
        sleep(0.1)
    raise TimeoutError()


@fixture(scope='session')
def docker_compose():
    filename = Path(__file__).parent.parent / 'docker-compose.yml'
    docker_compose_up = f'docker-compose -f {filename} up -d'
    check_call(docker_compose_up, shell=True)
    wait_until_responsive()
    try:
        yield
    finally:
        check_call(['docker-compose', 'down'])


@fixture
async def client(docker_compose) -> AsyncClient:
    async with AsyncClient(base_url='https://localhost', verify=False, http2=True) as client:
        yield client
