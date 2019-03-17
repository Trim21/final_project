import argparse
import logging
from types import FunctionType

from net_cloud.client import __version__, logger
from net_cloud.client.controllers import monitor, config
from . import init, initdb

ACTION_MAPS = {
    'initdb': initdb.main,
    'init': init.main,
    'config': config.main,
    'monitor': monitor.main
}


def main():
    c = argparse.ArgumentParser()
    c.add_argument('--verbosity', '-v', '--debug', help='more detail logging',
                   action='store_true', dest='debug')
    c.add_argument('--version', help='Show the version of BGmi.',
                   action='version', version=__version__)

    sub_parser = c.add_subparsers(help='actions', dest='action')

    init_parser = sub_parser.add_parser('init', help='init')
    initdb_parser = sub_parser.add_parser('initdb', help='initdb')
    config_parser = sub_parser.add_parser('config',
                                          help='write or print config')
    config_parser.add_argument('key', nargs='?',
                               type=lambda s: s.upper(),
                               # choices=cloud.client.config.__all_writable_now__
                               )
    config_parser.add_argument('value', nargs='?')
    monitor_parser = sub_parser.add_parser('monitor')

    ret = c.parse_args()
    if ret.debug:
        logger.setLevel(logging.DEBUG)
    func = ACTION_MAPS.get(ret.action)

    del ret.debug
    del ret.action

    if isinstance(func, FunctionType):
        func(**vars(ret))
