from typing import Callable, Awaitable, Optional, Dict, Mapping

import aioredis
import motor.core
import pymongo.results
import pytz
from aiohttp import web, ClientSession
from aiohttp_session import new_session, get_session, Session


class S:
    # login: bool
    # message: List
    # user info
    # nickname: Optional[str]
    # email: Optional[str]

    finish_register: Optional[bool]

    # auth token
    scope: Optional[None]
    user_id: Optional[int]
    auth_time: Optional[int]
    expires_in: Optional[int]
    token_type: Optional[str]
    access_token: Optional[str]
    refresh_token: Optional[str]

    # user info
    id: Optional[int]
    url: Optional[str]
    username: str
    nickname: str
    avatar: Optional[Dict[str, str]]
    sign: Optional[str]
    usergroup: Optional[int]

    # csrf
    csrf_token: Optional[str]
    csrf_time: Optional[int]
    __annotations__: dict


class ClassSession(S):
    # __annotations__ = S.__annotations__

    # _request = None
    # _session = None

    async def new_session(self) -> 'ClassSession':
        self._session = await new_session(self._request)
        self._request.session = self
        return self

    @classmethod
    async def from_request(cls, request: 'WebRequest'):
        session = await get_session(request)
        return cls(request, session)

    def __init__(self, request: 'WebRequest', session: Session):
        self._request = request
        self._session = session

    def __getattr__(self, item: str):
        if item not in S.__annotations__:
            raise AttributeError('{} is not a valid session key'.format(item))
        return self._session.get(item)

    def __setattr__(self, key, value):
        if key in ['_session', '_request']:
            object.__setattr__(self, key, value)
            return
        if key not in S.__annotations__:
            raise AttributeError(
                '{key} is not a valid session key, try to '
                'set session.{key} = `{value}`'.format(key=key, value=value)
            )
        self._session[key] = value

    def update(self, d: Mapping):
        for key, value in d.items():
            self.__setattr__(key, value)

    def __iter__(self):
        yield from self._session.items()

    def __repr__(self):
        return '<ClassSession {}'.format(self._session)

    def items(self):
        yield from self._session.items()

    __str__ = __repr__

    def to_dict(self):
        return self._session


class MongoCollection(motor.core.AgnosticCollection):
    update_one: Callable[[Dict, Dict], Awaitable[pymongo.results.UpdateResult]]


class TypeDatabase:
    token: MongoCollection
    user_auth: MongoCollection


class TypeMongoClient:
    net_cloud: TypeDatabase


class TypeApp(web.Application):
    tz: pytz.timezone
    db: TypeDatabase
    mongo: TypeMongoClient
    client_session: ClientSession
    redis: aioredis.Redis


class WebRequest(web.Request):
    app: TypeApp
    data: Optional[Dict]
    session: Optional[ClassSession]
