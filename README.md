YouTube Video Downloader & Merger (Python + FFmpeg)

This project downloads the highest-quality video and audio streams from a YouTube video and merges them into a single MP4 file using FFmpeg. It uses the pytubefix library to access adaptive streams and automatically generates a safe filename based on the video title.

Features:

  Downloads highest available video quality

  Downloads highest available audio quality

  Merges video and audio into one MP4 file

  Cleans video titles for valid filenames

  Automatically deletes temporary files

Requirements:

  Python 3.8 or higher

  FFmpeg

  pytubefix

  Install pytubefix:

  pip install pytubefix

Download FFmpeg:
  https://ffmpeg.org/download.html

Setup:

  Edit the script and update the following values.

Video URL:

  video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

FFmpeg path (Windows example):

  ffmpeg_path = r"Z:\your_path\ffmpeg.exe"

How It Works:

  Retrieves the highest resolution video stream

  Retrieves the highest bitrate audio stream

  Downloads both streams separately

  Merges them using FFmpeg

  Deletes temporary files

  Saves the final MP4 file

  Usage

Run the script:

  python downloader.py

Example output:

  Saved as: Video Title.mp4

  The file will be saved in the same directory as the script.

Why Separate Video and Audio?

  YouTube stores high-quality video and audio streams separately. Downloading and merging them results in better quality than downloading a single combined stream.

Future Improvements:

  Playlist support

Disclaimer:

  This project is for educational purposes only. Always respect YouTube’s Terms of Service and copyright laws.
