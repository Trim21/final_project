import time

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

from . import _config
from .handlers import Handler

import watchdog.tricks.ShellCommandTrick
# if __name__ == "__main__":


def m():
    if _config.SYNC_PATH is None:
        return
    # logging.basicConfig(level=logging.INFO,
    #                     format='%(asctime)s - %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')
    path = str(_config.SYNC_PATH)
    print('start watching {}'.format(path))
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.schedule(Handler(), path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
