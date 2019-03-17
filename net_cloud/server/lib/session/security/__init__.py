import enum

import motor.core
from aiohttp import web
from aiohttp_security.abc import AbstractAuthorizationPolicy, \
    AbstractIdentityPolicy
from aiohttp_session import get_session

IDENTITY_KEY = 'aiohttp_security_identity_policy'
AUTZ_KEY = 'aiohttp_security_autz_policy'


class Identity:
    login: bool
    username: str
    permission: str

    def __init__(self, username: str, login: bool, permission: str):
        self.username = username
        self.login = login
        self.permission = permission


class MongoAuthorizationPolicy(AbstractAuthorizationPolicy):
    """
    collection should have 3 fields,
    _id: str #username
    password: str #password
    permission: int #permission level
    """

    def __init__(self, mongo_collection: motor.core.AgnosticCollection):
        super().__init__()
        self.collection = mongo_collection

    async def authorized_userid(self, identity: Identity):
        """Retrieve authorized user id.
        Return the user_id of the user identified by the identity
        or 'None' if no user exists related to the identity.
        """
        if identity.login:
            return identity
        if await self.collection.find_one({'_id': identity, 'active': True}):
            return identity

    async def permits(self, identity, permission, context=None):
        """Check user permissions.
        Return True if the identity is allowed the permission in the
        current context, else return False.
        """
        # pylint: disable=unused-argument
        user = await self.collection.find_one({'_id': identity, 'login': True})
        if not user:
            return False
        return user.get('permission', 0) >= permission


class SessionIdentityPolicy(AbstractIdentityPolicy):

    def __init__(self, session_key='AIOHTTP_SECURITY'):
        self._session_key = session_key

    async def identify(self, request):
        session = await get_session(request)
        return session.get(self._session_key)

    async def remember(self, request, response, identity, **kwargs):
        session = await get_session(request)
        session[self._session_key] = identity

    async def forget(self, request, response):
        session = await get_session(request)
        session.pop(self._session_key, None)


async def remember(request, response, identity, **kwargs):
    """Remember identity into response.

    The action is performed by identity_policy.remember()

    Usually the identity is stored in user cookies somehow but may be
    pushed into custom header also.
    """
    assert isinstance(identity, Identity), identity
    assert identity
    identity_policy = request.config_dict.get(IDENTITY_KEY)
    if identity_policy is None:
        text = ("Security subsystem is not initialized, "
                "call aiohttp_security.setup(...) first")
        # in order to see meaningful exception message both: on console
        # output and rendered page we add same message to *reason* and
        # *text* arguments.
        raise web.HTTPInternalServerError(reason=text, text=text)
    await identity_policy.remember(request, response, identity, **kwargs)


async def forget(request, response):
    """Forget previously remembered identity.

    Usually it clears cookie or server-side storage to forget user
    session.
    """
    identity_policy = request.config_dict.get(IDENTITY_KEY)
    if identity_policy is None:
        text = ("Security subsystem is not initialized, "
                "call aiohttp_security.setup(...) first")
        # in order to see meaningful exception message both: on console
        # output and rendered page we add same message to *reason* and
        # *text* arguments.
        raise web.HTTPInternalServerError(reason=text, text=text)
    await identity_policy.forget(request, response)


async def authorized_userid(request):
    identity_policy = request.config_dict.get(IDENTITY_KEY)
    autz_policy = request.config_dict.get(AUTZ_KEY)
    if identity_policy is None or autz_policy is None:
        return None
    identity = await identity_policy.identify(request)
    if identity is None:
        return None  # non-registered user has None user_id
    user_id = await autz_policy.authorized_userid(identity)
    return user_id


async def permits(request, permission, context=None):
    assert isinstance(permission, (str, enum.Enum)), permission
    assert permission
    identity_policy = request.config_dict.get(IDENTITY_KEY)
    autz_policy = request.config_dict.get(AUTZ_KEY)
    if identity_policy is None or autz_policy is None:
        return True
    identity = await identity_policy.identify(request)
    # non-registered user still may has some permissions
    access = await autz_policy.permits(identity, permission, context)
    return access


async def is_anonymous(request):
    """Check if user is anonymous.

    User is considered anonymous if there is not identity
    in request.
    """
    identity_policy = request.config_dict.get(IDENTITY_KEY)
    if identity_policy is None:
        return True
    identity = await identity_policy.identify(request)
    if identity is None:
        return True
    return False


async def check_authorized(request):
    """Checker that raises HTTPUnauthorized for anonymous users.
    """
    userid = await authorized_userid(request)
    if userid is None:
        raise web.HTTPUnauthorized()
    return userid


async def check_permission(request, permission, context=None):
    """Checker that passes only to authoraised users with given permission.

    If user is not authorized - raises HTTPUnauthorized,
    if user is authorized and does not have permission -
    raises HTTPForbidden.
    """

    await check_authorized(request)
    allowed = await permits(request, permission, context)
    if not allowed:
        raise web.HTTPForbidden()


def setup(app, identity_policy, autz_policy):
    assert isinstance(identity_policy, AbstractIdentityPolicy), identity_policy
    assert isinstance(autz_policy, AbstractAuthorizationPolicy), autz_policy

    app[IDENTITY_KEY] = identity_policy
    app[AUTZ_KEY] = autz_policy
