import asyncio
import os
import pathlib

import aiohttp_jinja2
import aiohttp_security
import aiohttp_session
import jinja2
import pytz
from aiohttp import web, ClientSession

from net_cloud.server import db
from net_cloud.server.lib.types import WebRequest
from net_cloud.server.lib.session import RedisStorage
from net_cloud.server.lib.session.security import MongoAuthorizationPolicy, \
    Identity
from net_cloud.server.utils import load_session
from net_cloud.server.views import Lock, index
from net_cloud.server.views.auth import Login, Register

SERVER_DIR = pathlib.Path(os.path.dirname(__file__))


def redirect(location):
    async def r(request: WebRequest):
        raise web.HTTPFound(location)

    return r


async def clean_up(app: WebRequest.app):
    await app.client_session.close()
    await app.redis.close()


async def create_app(io_loop=asyncio.get_event_loop()):
    app = web.Application(

        # middlewares=[error_middleware, ]
    )
    app.tz = pytz.timezone('Asia/Shanghai')
    app.on_cleanup.append(clean_up)

    # setup http client session
    app.client_session = ClientSession(loop=io_loop)

    # setup database
    mongo_db = db.setup_mongo(app, io_loop)

    # setup session
    pool = await db.setup_redis(app, io_loop)
    import pickle
    aiohttp_session.setup(app, RedisStorage(pool,
                                            encoder=pickle.dumps,
                                            decoder=pickle.loads))
    # setup security
    identity_policy = aiohttp_security.SessionIdentityPolicy()
    authorization_policy = MongoAuthorizationPolicy(mongo_db['user_auth'])
    aiohttp_security.setup(app, identity_policy, authorization_policy)

    # setup template engine
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(SERVER_DIR / 'templates'))
    )
    app.add_routes([
        web.get('/', index),
        web.view('/login', Login),
        web.view('/register', Register),
        web.view('/lock.py', Lock),

    ])
    if os.getenv('D'):  # noqa pylint:disable=all
        import json
        import json.encoder

        class Encoder(json.encoder.JSONEncoder):
            def default(self, o):
                if isinstance(o, Identity):
                    return {'username': o.username,
                            'login': o.login,
                            'permission': o.permission}
                raise TypeError(f'Object of type {o.__class__.__name__} '
                                f'is not JSON serializable')

        async def show_session(request: WebRequest):
            await load_session(request)
            return web.json_response({
                key: value for key, value in request.session.items()
            }, dumps=lambda x: json.dumps(x, indent=2,
                                          ensure_ascii=False,
                                          cls=Encoder))

        app.add_routes([
            web.get('/dev/show_session', show_session),
        ])

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    web.run_app(create_app(io_loop=loop), port=6003)
