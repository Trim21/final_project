import logging

from ._config import config
from ._logger import logger
from .setup import ensure_dirs_exists, setup

__version__ = '1.1.1'
__all__ = ['logger', 'config']

setup()

try:
    h = logging.FileHandler(config.path.log_file)
    logger.addHandler(h)
except IOError:
    logger.warning('can\'t save log output to log file')
