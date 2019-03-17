from watchdog.events import FileSystemEventHandler


class Handler(FileSystemEventHandler):
    def on_moved(self, event):
        print(event)

    def on_deleted(self, event):
        print(event)

    def on_created(self, event):
        print(event)

    def on_modified(self, event):
        print(event)
