import time
import asyncio
from queue import Queue
from watchdog.observers import Observer
from handler import MyEventHandler

class Watcher:

    def __init__(self, path):
        self.path = path
        self.observer = Observer()
        self.handler = MyEventHandler(path)

    def start(self):
        self.observer.schedule(self.handler, self.path, recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    async def run(self):
        self.start()
        try:
            while self.observer.is_alive():
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            self.stop()
