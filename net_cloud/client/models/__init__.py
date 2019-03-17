from net_cloud.client import logger
from ._base import db
from .dirs import Dirs
from .files import Files


def create_tables():
    logger.info('init db')
    db.connect()
    Files.create_table()
    Dirs.create_table()
    db.close()


__all__ = ['db', 'Dirs', 'Files', 'create_tables']
