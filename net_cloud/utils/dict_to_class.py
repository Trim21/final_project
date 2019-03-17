from functools import reduce
from pathlib import Path

APP_HOME = Path('/')

config_dict = {
    'lang': 'zh_cn',
    'is_windows': True,
    'path': {
        'app_home': 1,
        'db': 2,
        'tools_dir': 3,
        'tmp_dir': 4,
        'front_static_dir': Path('/front_static'),
        'sync_dir': None,
        'config_file': Path('/config.toml'),
        'log_file': Path('/cloud.log'),
    }
}


class config:
    LANG = 'zh_cn'
    IS_WINDOWS = True

    class path:
        APP_HOME = Path('/')

        DB = APP_HOME / 'cloud.db'

        TOOLS_DIR = APP_HOME / 'tools'
        TMP_DIR = APP_HOME / 'tmp'
        FRONT_STATIC_DIR = APP_HOME / 'front_static'
        SYNC_DIR = None

        CONFIG_FILE = APP_HOME / 'config.toml'
        LOG_FILE = APP_HOME / 'cloud.log'


def get_class_member_dict(obj: object):
    d = {}
    for key, value in obj.__dict__.items():
        if isinstance(value, classmethod):
            continue
        if key.startswith('_'):
            continue
        if isinstance(value, object.__class__):
            d[key] = get_class_member_dict(value)
        else:
            d[key] = value
    return d


def merge_dict_to_class(d: dict, obj: object):
    for key, value in d.items():
        # merge dict to <class 'type'> or dict
        if isinstance(value, dict):
            obj_value = getattr(obj, key, None)
            if isinstance(obj_value, dict):
                setattr(obj, key, value)
            elif isinstance(obj_value, object.__class__):
                merge_dict_to_class(value, obj_value)
            else:
                raise TypeError(
                    'try to update a single value `{}` with dict '.format(key)
                )

        else:
            setattr(obj, key, value)


def rec_getattr(obj, attr):
    return reduce(getattr, attr.split('.'), obj)


def rec_setattr(obj, attr, value):
    attrs = attr.split('.')
    setattr(reduce(getattr, attrs[:-1], obj), attrs[-1], value)
