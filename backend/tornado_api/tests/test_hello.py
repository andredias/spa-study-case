import json

from pytest import mark
from tornado.simple_httpclient import SimpleAsyncHTTPClient


@mark.gen_test
async def test_hello(http_client: SimpleAsyncHTTPClient, base_url) -> None:
    response = await http_client.fetch(f'{base_url}/hello')
    data = json.loads(response.body)
    assert data == {'hello': 'world'}
