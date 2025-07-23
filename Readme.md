https://github.com/user-attachments/assets/80c83c6b-6e48-471f-8bf0-7d7adc10a89e


# gitSync/watchDawg

**watchDawg** is a filesystem event monitoring tool built with Python’s `watchdog` library. It monitors file system changes, logs them, and generates Git commands to track modifications.

> ⚠️ **Note:** Git commands are currently only being generated, not executed.

---

## 📝 How it Works

- Detects filesystem events (e.g., file edits, creation, deletion).
- Logs detailed event data to help identify how different apps (like `nvim`) interact with files.
- Avoids committing or pushing temporary or irrelevant files by learning app-specific patterns.
- Aims to support periodic `git add`, `commit`, and `push` to a specified remote in future versions.

---

## 🔍 Current Status

This tool is currently in a **data-gathering phase**. It only logs events to help fine-tune the filtering logic.  
Execution of actual Git commands (`add`, `commit`, `push`) is **not yet enabled**.

---

## 🚀 Release Info

A **Windows executable** is available, built using **PyInstaller**.
