# coding=utf-8
import os
'中文'
import platform
from pathlib import Path

import toml

from net_cloud.utils.dict_to_class import get_class_member_dict, rec_setattr, \
    merge_dict_to_class


# from ._logger import logger


def get_app_home():
    if not os.environ.get('BGMI_PATH'):
        if platform.system() == 'Windows':
            _BGMI_PATH = os.environ.get('USERPROFILE', None)
        else:
            _BGMI_PATH = os.environ.get('USER_HOME', '/tmp')
    else:  # pragma: no cover
        _BGMI_PATH = os.environ.get('BGMI_PATH')
    return Path(_BGMI_PATH) / 'net_cloud'


_app_home = get_app_home()
default_config_dict = {
    'lang': 'zh_cn',
    'log_level': 'INFO',
    'path': {
        'tools_dir': str(_app_home / 'tools'),
        'tmp_dir': str(_app_home / 'tmp'),
        'front_static_dir': str(_app_home / 'front_static'),
        # 'sync_dir': '',
        # 'log_file': str(_app_home / 'cloud.log'),
    },
    'log_config': {
        'version': 1,
        'formatters': {
            'precise': {
                'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
            },
            'brief': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'brief',
                'level': 'INFO',
                # 'filters': '[allow_foo]',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'precise',
                'filename': str(_app_home / 'tmp' / 'net_cloud.log'),
                'maxBytes': 1024,
                'backupCount': 3
            }
        },
        'loggers': {
            'net_cloud': {
                'handlers': ['console', 'file'],
                'propagate': True,
                'level': 'INFO',
            }
        }
    }
}


# readonly_config_dict = {
#     'is_windows': platform.system() == 'Windows',
#     'path': {
#         'db': _app_home / 'cloud.db',
#         'config_file': _app_home / 'config.toml',
#     }
# }


class config:
    lang = 'zh_cn'
    is_windows = platform.system() == 'Windows'

    class path:
        app_home = get_app_home()

        db = app_home / 'cloud.db'

        tools_dir = app_home / 'tools'
        tmp_dir = app_home / 'tmp'
        front_static_dir = app_home / 'front_static'
        sync_dir = None

        config_file = app_home / 'config.toml'
        log_file = app_home / 'cloud.log'

    log_config = {}

    @classmethod
    def to_dict(cls):
        return get_class_member_dict(cls)


def read_config():
    try:
        with open(config.path.config_file, 'r+', encoding='utf-8') as f:
            user_config = toml.load(f)
            for key, value in user_config.get('path', {}).items():
                user_config['path'][key] = Path(value)
            merge_dict_to_class(user_config, config)
    except FileNotFoundError:
        pass
        # write_default_config()


def print_config():
    return toml.dumps(config.to_dict())


def write_default_config():
    # logger.info('write default config')
    print('write default config')
    with open(config.path.config_file, 'w+', encoding='utf-8') as f:
        toml.dump(default_config_dict, f)


def write_config(key=None, value=None):
    rec_setattr(config, key, value)
    with open(config.path.config_file, 'w+', encoding='utf-8') as f:
        toml.dump(config.to_dict(), f, )


# ------------------------------ #
# !!! Read config from file and write to globals() !!!
read_config()

if __name__ == '__main__':
    pass
