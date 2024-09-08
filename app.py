"""
This module creates a GUI using tkinter to:
- Browse for a video file (mp4, avi, or mkv)
- Execute a function to remove silent parts from the video
"""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from moviepy.editor import VideoFileClip
from silence import find_speaking, get_keep_clips, remove_silence


# Initialize the Tkinter GUI
root = tk.Tk()
root.title("Remove Silence from Video")

# Get the current working directory
cwd = Path.cwd()

# Create a frame for the input file selection
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

input_label = tk.Label(input_frame, text="Input Video File:")
input_label.pack(side=tk.LEFT)

entry_input = tk.Entry(input_frame, width=50)
entry_input.pack(side=tk.LEFT)

def browse_input():
    file_path = filedialog.askopenfilename(initialdir=cwd)
    entry_input.delete(0, tk.END)
    entry_input.insert(0, file_path)

browse_button_input = tk.Button(input_frame, text="Browse", command=browse_input)
browse_button_input.pack(side=tk.LEFT)

# Create a frame for the output file selection
output_frame = tk.Frame(root)
output_frame.pack(pady=5)

output_label = tk.Label(output_frame, text="Output Video File:")
output_label.pack(side=tk.LEFT)

entry_output = tk.Entry(output_frame, width=50)
entry_output.pack(side=tk.LEFT)

def browse_output():
    file_path = filedialog.asksaveasfilename(initialdir=cwd)
    entry_output.delete(0, tk.END)
    entry_output.insert(0, file_path)

browse_button_output = tk.Button(output_frame, text="Browse", command=browse_output)
browse_button_output.pack(side=tk.LEFT)

# Create a button to remove silence from the video
def remove_silence_from_video():
    file_in = entry_input.get()
    file_out = entry_output.get()

    vid = VideoFileClip(file_in)
    intervals_to_keep = find_speaking(vid.audio)
    keep_clips = get_keep_clips(vid, intervals_to_keep)
    remove_silence(keep_clips, file_out)
    vid.close()

remove_button = tk.Button(root, text="Remove Silence", command=remove_silence_from_video)
remove_button.pack(pady=10)

# Run the main loop
root.mainloop()