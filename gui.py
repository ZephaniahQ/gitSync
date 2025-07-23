import time
import os
import tkinter as tk
from tkinter import filedialog,ttk
import asyncio
import threading
from watcher import Watcher
from logviewer import LogViewer

LOG_FILE = "log.txt"

watcher = None
watcher_thread = None
watching = False

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
       path_var.set(folder) 

def run_asyncio_watcher(path):
    global watcher
    watcher = Watcher(path)
    
    async def runner():
        await watcher.run()

    asyncio.run(runner())

def start_watcher():
    global watcher_thread
    path = path_var.get()
    if path:
        watcher_thread = threading.Thread(target=run_asyncio_watcher, args=(path,), daemon=True)
        watcher_thread.start()

def stop_watcher():
    if watcher:
        watcher.stop()

def toggle_run():
    global watching
    if not watching:
        run_btn.config(text="Stop")
        start_watcher()
        gitLog.start()
        rawLog.start()
    else:
        run_btn.config(text="Run")
        stop_watcher()
        gitLog.stop()
        rawLog.stop()
    watching = not watching

root = tk.Tk()
root.title("WatchDawg")
root.geometry("1280x720")
path_var = tk.StringVar()

#Frame for top controls
top_frame = tk.Frame(root)
top_frame.pack(pady=10, fill="x", padx=10)

#select folder button

select_btn = tk.Button(top_frame, text="Select Folder", command=select_folder)
select_btn.grid(row=0, column=0, sticky="w")

#label to display the path
path_label = tk.Label(top_frame, textvariable=path_var, wraplength=350, relief="sunken", anchor="w")
path_label.grid(row=0, column=1, padx=5, sticky="ew")

#run button

run_btn = tk.Button(top_frame, text = "Run", command=toggle_run)
run_btn.grid(row=0,column=2,sticky="e")

#make path label expand when window resizes
top_frame.grid_columnconfigure(1,weight=1)

log_frame = tk.Frame(root)
log_frame.pack(fill="both",expand=True,padx=10)

log_frame.columnconfigure(0, weight=1)
log_frame.columnconfigure(1, weight=1)
log_frame.rowconfigure(0, weight=1)

gitLog = LogViewer(log_frame, "log.txt", title="Git Log")
gitLog.grid(row=0,column=0, sticky="nsew", padx=(0,5))

rawLog = LogViewer(log_frame, "rawlog.txt", title="Event log")
rawLog.grid(row=0,column=1,sticky="nsew",padx=(5,0))

root.mainloop()
