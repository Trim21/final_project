import json
from typing import Type

from aiohttp import web
from validator import Validator

from net_cloud.server.lib.types import WebRequest, ClassSession


async def load_session(request: WebRequest):
    request.session = await ClassSession.from_request(request)


def valid(validator: Type[Validator], raw_data):
    v = validator(dict(raw_data))
    if v.is_valid():
        return v.validated_data
    raise web.HTTPBadRequest(reason=json.dumps(v.str_errors))
