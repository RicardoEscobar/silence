#!/usr/bin/env python
#
# Based on a script by Donald Feury
# https://gitlab.com/dak425/scripts/-/blob/master/trim_silenceV2
# https://youtu.be/ak52RXKfDw8

import math
import sys
import subprocess
import os
import shutil
from pathlib import Path
from moviepy.editor import AudioClip, VideoFileClip, concatenate_videoclips


# Iterate over audio to find the non-silent parts. Outputs a list of
# (speaking_start, speaking_end) intervals.
# Args:
#  window_size: (in seconds) hunt for silence in windows of this size
#  volume_threshold: volume below this threshold is considered to be silence
#  ease_in: (in seconds) add this much silence around speaking intervals
def find_speaking(audio_clip, window_size=0.1, volume_threshold=0.01, ease_in=0.25):
    # First, iterate over audio to find all silent windows.
    num_windows = math.floor(audio_clip.end / window_size)
    window_is_silent = []
    for i in range(num_windows):
        s = audio_clip.subclip(i * window_size, (i + 1) * window_size)
        v = s.max_volume()
        window_is_silent.append(v < volume_threshold)

    # Find speaking intervals.
    speaking_start = 0
    speaking_end = 0
    speaking_intervals = []
    for i in range(1, len(window_is_silent)):
        e1 = window_is_silent[i - 1]
        e2 = window_is_silent[i]
        # silence -> speaking
        if e1 and not e2:
            speaking_start = i * window_size
        # speaking -> silence, now have a speaking interval
        if not e1 and e2:
            speaking_end = i * window_size
            new_speaking_interval = [speaking_start - ease_in, speaking_end + ease_in]
            # With tiny windows, this can sometimes overlap the previous window, so merge.
            need_to_merge = (
                len(speaking_intervals) > 0
                and speaking_intervals[-1][1] > new_speaking_interval[0]
            )
            if need_to_merge:
                merged_interval = [speaking_intervals[-1][0], new_speaking_interval[1]]
                speaking_intervals[-1] = merged_interval
            else:
                speaking_intervals.append(new_speaking_interval)

    return speaking_intervals


def get_keep_clips(vid, intervals_to_keep):
    return [vid.subclip(max(start, 0), end) for [start, end] in intervals_to_keep]


def get_fps(file_path: Path) -> int:
    """Get the frames per second of a video file."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=r_frame_rate",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(file_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    fps = result.stdout.decode("utf-8").split("/")
    return int(fps[0]) / int(fps[1])


def remove_silence(
    keep_clips,
    file_out,
    fps=60,
    preset="ultrafast",
    codec="libx264",
    temp_audiofile="temp-audio.m4a",
    remove_temp=True,
    audio_codec="aac",
    threads=6,
):
    edited_video = concatenate_videoclips(keep_clips)
    edited_video.write_videofile(
        str(file_out),
        fps=fps,
        preset=preset,
        codec=codec,
        temp_audiofile=temp_audiofile,
        remove_temp=remove_temp,
        audio_codec=audio_codec,
        threads=threads,
    )


def remove_silence_from_video(file_in: Path, file_out: Path):
    """Given an input video file and an output file, remove silence from the video."""
    vid = VideoFileClip(str(file_in))
    intervals_to_keep = find_speaking(vid.audio)
    keep_clips = get_keep_clips(vid, intervals_to_keep)
    fps = get_fps(file_in)
    remove_silence(keep_clips, file_out, fps)
    vid.close()


def remove_silence_dir(dir: Path):
    """Given a given directory, remove silence from all the videos in it."""
    # if the directory is empty, raise an error
    if not any(dir.iterdir()):
        raise ValueError("The directory is empty.")

    for file in dir.iterdir():
        if file.suffix in [".mp4", ".avi", ".mov", ".mkv"]:
            # Create a new directory to store the processed video
            output_dir = dir / "no_silence"
            output_dir.mkdir(exist_ok=True)

            # Process the video
            output_path = output_dir / file.name
            remove_silence_from_video(file, output_path)


def main_single_file():
    # Parse args
    # Input file path
    file_in = sys.argv[1]
    # Output file path
    file_out = sys.argv[2]

    vid = VideoFileClip(file_in)
    intervals_to_keep = find_speaking(vid.audio)

    print("Keeping intervals: " + str(intervals_to_keep))

    # Get the clips to keep
    keep_clips = get_keep_clips(vid, intervals_to_keep)

    # TODO: Refactor this to a function
    remove_silence(keep_clips, file_out)

    vid.close()


def main_dir():
    # Parse args
    # Input directory path
    dir_in = Path(sys.argv[1])

    remove_silence_dir(dir_in)


def main():
    if len(sys.argv) == 3:
        main_single_file()
    elif len(sys.argv) == 2:
        main_dir()
    else:
        print("Usage: python silence.py <input_file> <output_file>")
        print("Usage: python silence.py <input_dir>")


if __name__ == "__main__":
    main()
