import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    DIRECTORY_TO_WATCH = "."

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler(12, 7)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    points_to_calculate = 50
    points_to_show = 15

    def __init__(self, points_to_calculate, points_to_show):
        self. points_to_calculate = points_to_calculate
        self.points_to_show = points_to_show

    
    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print ("Received created event - %s." % event.src_path)

            print("num_calc: " + str(self.points_to_calculate))
            print("num_show: " + str(self.points_to_show))

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print ("Received modified event - %s." % event.src_path)


if __name__ == '__main__':
    w = Watcher()
    w.run()