import aiohttp_jinja2
from aiohttp import web

from net_cloud.server import utils
from net_cloud.server.lib.types import WebRequest
from net_cloud.server.lib.session.security import remember, Identity
from net_cloud.server.utils import valid
from net_cloud.server.validators import RegisterValidator, LoginValidator


class Login(web.View):
    request: WebRequest

    async def get(self):
        return aiohttp_jinja2.render_template('login.html', self.request, {})

    async def post(self):
        data = utils.valid(LoginValidator, await self.request.post())
        resp = web.Response(text='hello')
        user = await self.request.app.db.user_auth \
            .find_one({'_id': data['username'],
                       'password': data['password']})
        if user:
            await remember(
                self.request,
                resp,
                Identity(data['username'], True, user['permission'])
            )
            return resp
        return web.HTTPUnauthorized(reason='username and password mismatch')


class Register(web.View):
    request: WebRequest

    async def get(self):
        return aiohttp_jinja2.render_template('register.html', self.request, {})

    async def post(self):
        data = utils.valid(RegisterValidator, await self.request.post())
        w = await self.request.app.db.user_auth.update_one(
            {'_id': self.request.data['username']},
            {'$setOnInsert': {'password': data['password'],
                              'active': True}},
            upsert=True
        )
        if w.modified_count:
            return web.json_response({'status': 'success'})
        return web.json_response({'status': 'error', 'message': 'user exists'})


class Token(web.View):
    request: WebRequest

    async def get(self):
        return aiohttp_jinja2.render_template('register.html', self.request, {})

    async def post(self):
        data = valid(RegisterValidator, await self.request.post())
        w = await self.request.app.db.user_auth.update_one(
            {'_id': self.request.data['username']},
            {'$setOnInsert': {'password': data['password'],
                              'active': True}},
            upsert=True
        )
        if w.modified_count:
            return web.json_response({'status': 'success'})
        return web.json_response({'status': 'error', 'message': 'user exists'})
