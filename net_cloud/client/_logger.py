import logging
import logging.config

from ._config import config


def get_logger():
    if config.log_config:
        logging.config.dictConfig(config.log_config)
    _logger = logging.getLogger('net_cloud')
    return _logger


logger = get_logger()
