import aiohttp_jinja2
from aiohttp import web

from net_cloud.server.lib.types import WebRequest
from net_cloud.server.lib.session.security import check_authorized
from net_cloud.server.utils import load_session


class Lock(web.View):
    request: WebRequest

    async def get(self):
        await load_session(self.request)
        await check_authorized(self.request)
        return web.Response(text=self.request.method)

    async def post(self):
        await check_authorized(self.request)
        return web.Response(text=self.request.method)


async def index(request: WebRequest):
    await load_session(request)
    return aiohttp_jinja2.render_template('index.html', request, {})
    # return web.Response(
    #     text=await request.app.redis.get('key2', 'default value')
    # )
