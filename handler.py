from watchdog.events import FileSystemEvent, FileSystemEventHandler
import os 
from datetime import datetime

class MyEventHandler(FileSystemEventHandler):

    def __init__(self, toWatch):
        self.toWatch = toWatch

    def getName(self, src_path):
        return os.path.relpath(src_path, start=self.toWatch)

    def rawlog(self, event):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        rawlogfile = "rawlog.txt"
        rawlogdir =  os.path.dirname(rawlogfile)
        if rawlogdir:
            os.makedirs((rawlogfile), exist_ok=True)
        name = self.getName(event.src_path)
        with open(rawlogfile, 'a') as f:
            f.write(timestamp + f" type: {event.event_type} path: {name}" + "\n")

    def log(self, command):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        logfile = "log.txt"
        logdir = os.path.dirname(logfile)
        if logdir:
            os.makedirs((logfile), exist_ok=True)
        with open(logfile, 'a') as f:
            f.write(timestamp + " " + command + "\n")


    def on_any_event(self, event):
        self.rawlog(event)

    def on_created(self, event):
        if event.is_directory:
            return
        name = self.getName(event.src_path)
        command = f"git add {name}"
        print(command)
        self.log(command)

    def on_modified(self, event):
        if event.is_directory:
            return
        name = self.getName(event.src_path)
        command = f"git commit -m \"{name} modified\""
        print(command)
        self.log(command)




    
