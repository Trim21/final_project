import os
from os import path

from net_cloud.client._config import write_config


def main(key=None, value=None):
    if key.endswith('_PATH'):
        if not path.isabs(value):
            value = path.join(os.getcwd(), value)
    result = write_config(key, value)
    print(result['message'])
