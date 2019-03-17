import os
from urllib.parse import quote_plus

APP_ID = os.environ.get('APP_ID')
APP_SECRET = os.environ.get('APP_SECRET')
# if not (APP_SECRET and APP_ID):
#     raise EnvironmentError('you must set env APP_ID and APP_SECRET')

HOST = os.environ.get('HOST', 'localhost:6001')
PROTOCOL = os.environ.get('PROTOCOL', 'http')


class MongoConfig:
    host = os.environ.get('MONGO_HOST', '127.0.0.1')
    port = os.environ.get('MONGO_PORT', '27017')
    username = os.environ.get('MONGO_USERNAME', '')
    password = os.environ.get('MONGO_PASSWORD', '')

    db_name = os.environ.get('MONGO_DATABASE', 'net_cloud')

    class Collection:
        user_auth = 'user_auth'

    if username and password:
        mongo_url = f"mongodb://{quote_plus(username)}:{quote_plus(password)}" \
            f"@{host}:{port}/{db_name}"
    else:
        mongo_url = f"mongodb://{host}:{port}/{db_name}"


class RedisConfig:
    host = os.getenv('REDIS_HOST', 'nas.acg.tools')
    port = os.getenv('REDIS_PORT', '6379')
    db = os.getenv('REDIS_DB', '0')
    password = os.getenv('REDIS_PASSWORD')
    connect_url = 'redis://{host}:{port}/{db}'.format(
        host=host,
        port=port,
        db=db,
    )
