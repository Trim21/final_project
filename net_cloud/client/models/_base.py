# pylint: disable=R0903
import peewee as pw

from net_cloud.client import logger, config

db = pw.SqliteDatabase(str(config.path.db))


class BaseModel(pw.Model):
    class Meta:
        database = db

    @classmethod
    def create_table(cls, safe=True, **options):
        logger.debug('creating table %s', cls.__name__)
        super(BaseModel, cls).create_table(safe=safe, **options)
