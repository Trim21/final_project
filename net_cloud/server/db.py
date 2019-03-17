import asyncio

import aioredis
from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from net_cloud.server import config


# from .bass_class import Redis


def setup_mongo(app, loop):
    mongo = AsyncIOMotorClient(
        config.MongoConfig.mongo_url, maxPoolSize=10, io_loop=loop)
    app.mongo = mongo
    app.db = mongo[config.MongoConfig.db_name]
    return app.db


async def setup_redis(app: web.Application, io_loop: asyncio.AbstractEventLoop):
    pool = await aioredis.create_redis_pool(
        config.RedisConfig.connect_url,
        password=config.RedisConfig.password,
        minsize=5,
        maxsize=20,
        loop=io_loop,
        # commands_factory=Redis,
        # encoding='utf-8'
    )
    app.redis = pool
    return pool
