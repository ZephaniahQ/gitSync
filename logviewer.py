import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext 
import asyncio
import threading
import os
import time
from datetime import datetime

class LogViewer(tk.Frame):
    def __init__(self, master, log_file, title="Log", **kwargs):
        super().__init__(master,**kwargs)
        self.log_file = log_file
        self.last_size = 0

        # Heading frame

        heading_frame = ttk.Frame(self)
        heading_frame.pack(fill="x", pady=(5,0))

        label = ttk.Label(heading_frame, text=title, font=("Arial", 12,"bold"))
        label.pack(side="left")

        clear_btn = ttk.Button(heading_frame, text="Clear", command=self.clear)
        clear_btn.pack(side="right")

        #Text box

        self.textbox = scrolledtext.ScrolledText(self, wrap=tk.WORD, height = 10)
        self.textbox.pack(fill="both", expand=True,pady=(0,10))

        self.textbox.config(state="disabled")

        self.running = False;
        self.thread = None

    def _tail(self):
        while self.running:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    f.seek(self.last_size)
                    new_data = f.read()
                    if new_data:
                        self.textbox.config(state="normal")
                        self.textbox.insert(tk.END, new_data)
                        self.textbox.see(tk.END)
                        self.textbox.config(state="disabled")
                        self.last_size = f.tell()
            time.sleep(0.5)

    def start(self):
        if not self.running:
            self.running = True
            with open(self.log_file, 'a') as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"\n[INFO] Started logging at {timestamp}\n")
            self.thread = threading.Thread(target=self._tail, daemon=True)
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            if os.path.exists(self.log_file):
                with open(self.log_file, 'a') as f:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"\n[INFO] Stopped logging at {timestamp}\n")


    def clear(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        self.textbox.config(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.config(state="disabled")
