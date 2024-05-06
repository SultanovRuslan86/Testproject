from aiohttp import web
import hashlib
import click
import json


async def healthcheck(request):
    return web.Response(status=200, text=json.dumps({}))


async def hash_string(request):
    try:
        data = await request.json()
        string_to_hash = data['string']
        hash_object = hashlib.sha256(string_to_hash.encode())
        hash_hex = hash_object.hexdigest()
        return web.Response(status=200, text=json.dumps({'hash_string': hash_hex}))
    except KeyError:
        return web.Response(status=400, text=json.dumps({'validation_errors': 'Field "string" is missed'}))


@click.command()
@click.option('--port', default=8080, help='Port to listen on')
def run_server(port):
    app = web.Application()
    app.router.add_get('/healthcheck', healthcheck)
    app.router.add_post('/hash', hash_string)
    web.run_app(app, port=port)


if __name__ == '__main__':
    run_server()

