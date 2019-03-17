from os import makedirs

from ._config import config, write_default_config
from ._logger import logger


def ensure_dirs_exists():
    create_dir = False
    for dir_path in [
        config.path.app_home,
        config.path.tmp_dir,
        config.path.tools_dir,
    ]:
        if dir_path.exists():
            logger.debug('%s exists, skip for creating', str(dir_path))
        else:
            create_dir = True
            logger.info('%s does not exist, creating', str(dir_path))
            makedirs(str(dir_path))
    return create_dir


def setup():
    if ensure_dirs_exists():
        write_default_config()
