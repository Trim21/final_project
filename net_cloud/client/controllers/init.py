from net_cloud.client import _config
from net_cloud.client import logger
from net_cloud.client import setup
from . import initdb


def main():
    logger.info('create home dir')
    setup.ensure_dirs_exists()
    logger.info('write default config file')
    _config.write_default_config()
    initdb.create_tables()
