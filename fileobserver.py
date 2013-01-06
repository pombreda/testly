import time

# Import Watchdog for monitoring the filesystem
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print 'Watchdog module not installed. File watch functionality disabled'
    exit(7)


# Override the base event handler class to run the tests when the files change
class TestEventHandler(FileSystemEventHandler):
    def __init__(self, callback):
        FileSystemEventHandler.__init__(self)
        self.callback = callback

    def on_modified(self, event):
        self.callback()


class FileObserver:
    def __init__(self, callback, paths_to_watch=None):
        # Get the array of paths to watch from the JSON file
        default_paths = [
            {
                'path': '.',
                'recursive': True
            }
        ]
        if paths_to_watch == None:
            paths_to_watch = default_paths

        if len(paths_to_watch) < 1:
            print '"watch" property in tests.json is empty'
            exit(6)

        # Create an instance of the new event handler and an observer
        event_handler = TestEventHandler(callback)
        self.observer = Observer()

        # Register the event for each path in the array
        for path in paths_to_watch:
            path_string = path['path'] if 'path' in path else '.'
            recursive = path['recursive'] if 'recursive' in path else True

            self.observer.schedule(event_handler, path=path_string,
                recursive=recursive)

    def observe(self):
        # Start watching changes
        print 'Watching for changes. Press Ctrl+C to cancel'
        self.observer.start()

        # Allow the monitoring loop to be interrupted by a keyboard event
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
