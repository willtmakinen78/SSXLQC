import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler

if __name__ == "__main__":

    event_handler = _RFHandler(12, 7)
    DIRECTORY_TO_WATCH = sys.argv[1] if len(sys.argv) > 1 else '.'
    self.observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
    self.observer.start()
    try:
        print("rf folder monitor starting")
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        self.observer.stop()
        print("rf watcher exiting")

    self.observer.join()


    # logging.basicConfig(level=logging.INFO,
    #                     format='%(asctime)s - %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')
    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    # event_handler = LoggingEventHandler()
    # observer = Observer()
    # observer.schedule(event_handler, path, recursive=True)
    # observer.start()
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()
    # observer.join()

class _RFHandler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(self, event):
        if event.is_directory:
            return None

        # called when a file is first created/moved to tge folder
        elif event.event_type == 'created':
            print("num_calc: " + str(self.num_calc))
            print("num_show: " + str(self.num_show))