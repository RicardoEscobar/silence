"""
This module creates a GUI using tkinter to:
- Browse for a directory containing (mp4, avi, or mkv) video files.
- Execute a function to remove silent parts from the videos.
"""
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from silence import remove_silence_dir


def browse_dir():
    dir = filedialog.askdirectory(initialdir=cwd)
    dir_path = Path(dir)
    print(f"Selected directory: {dir_path} as string: {str(dir_path)}")
    entry_dir.delete(0, tk.END)
    entry_dir.insert(0, str(dir_path))


def remove_silence_from_dir():
    dir = entry_dir.get()
    dir_path = Path(dir)
    try:
        remove_silence_dir(dir_path)
    except ValueError as e:
        print(e)
        return

# Initialize the Tkinter GUI.
root = tk.Tk()

# Set the title of the GUI
root.title("Remove Silence from Videos in Directory")

# Get the current working directory
cwd = Path.cwd()

# Create a frame for the directory selection
dir_frame = tk.Frame(root)
dir_frame.pack(pady=5)

dir_label = tk.Label(dir_frame, text="Input Directory:")
dir_label.pack(side=tk.LEFT)

entry_dir = tk.Entry(dir_frame, width=50)
entry_dir.pack(side=tk.LEFT)

# Create a button to browse for the directory
browse_button = tk.Button(dir_frame, text="Browse", command=browse_dir)
browse_button.pack(side=tk.LEFT)

# Create a button to remove silence from the videos in the directory
remove_button = tk.Button(root, text="Remove Silence from Videos", command=remove_silence_from_dir)
remove_button.pack(pady=5)

# Run the Tkinter main loop
root.mainloop()
