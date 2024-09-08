"""
This module creates a GUI using tkinter to:
- Browse for a video file (mp4, avi, or mkv)
- Execute a function to remove silent parts from the video
"""

import tkinter as tk

from moviepy.editor import VideoFileClip

from silence import find_speaking, get_keep_clips, remove_silence


# Create the main window
root = tk.Tk()
root.title("Remove Silence from Video")

# Create a label for the input file path
label_input = tk.Label(root, text="Input file path:")
label_input.pack()

# Create a text entry for the input file path
entry_input = tk.Entry(root)
entry_input.pack()

# Create a label for the output file path
label_output = tk.Label(root, text="Output file path:")
label_output.pack()

# Create a text entry for the output file path
entry_output = tk.Entry(root)
entry_output.pack()

# Create a button to browse for the input file
def browse_input():
    file_path = tk.filedialog.askopenfilename()
    entry_input.delete(0, tk.END)
    entry_input.insert(0, file_path)

browse_button_input = tk.Button(root, text="Browse", command=browse_input)
browse_button_input.pack()

# Create a button to browse for the output file
def browse_output():
    file_path = tk.filedialog.asksaveasfilename()
    entry_output.delete(0, tk.END)
    entry_output.insert(0, file_path)

browse_button_output = tk.Button(root, text="Browse", command=browse_output)
browse_button_output.pack()

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
remove_button.pack()

# Run the main loop
root.mainloop()
