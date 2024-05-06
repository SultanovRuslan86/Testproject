from aiohttp import web
import pytest
from server import healthcheck, hash_string


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    app.router.add_get('/healthcheck', healthcheck)
    app.router.add_post('/hash', hash_string)
    return loop.run_until_complete(aiohttp_client(app))


async def test_healthcheck(cli):
    resp = await cli.get('/healthcheck')
    assert resp.status == 200
    text = await resp.text()
    assert text == '{}'


async def test_hash_string(cli):
    resp = await cli.post('/hash', json={'string': 'test'})
    assert resp.status == 200
    text = await resp.text()
    json_resp = json.loads(text)
    assert 'hash_string' in json_resp


async def test_hash_string_error(cli):
    resp = await cli.post('/hash', json={})
    assert resp.status == 400
    text = await resp.text()
    json_resp = json.loads(text)
    assert 'validation_errors' in json_resp