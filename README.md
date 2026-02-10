# YouTube Video Downloader & Merger

A Python application that downloads the highest-quality video and audio streams from YouTube and merges them into a single MP4 file using FFmpeg.

---

## Features

- High-resolution video download
- High-bitrate audio download
- Automatic stream merging with FFmpeg
- Safe filename generation
- Temporary file cleanup
- GUI with live progress bars

---

## Requirements

- Python 3.8+
- FFmpeg
- pytubefix

---

## Installation

Install pytubefix:

pip install pytubefix

Download FFmpeg:
https://ffmpeg.org/download.html

---

## Setup

Open the script and update the FFmpeg path.

Example (Windows):

ffmpeg_path = r"Z:\your_path\ffmpeg.exe"

---

## Usage

Run the application:

python YoutubeDownloader.py

Saved output example:

C:\Videos\My Video Title.mp4

---

## How It Works

1. Selects highest-resolution video stream
2. Selects highest-bitrate audio stream
3. Downloads streams separately
4. Merges using FFmpeg
5. Deletes temporary files
6. Saves final MP4

---

## Why Video and Audio Are Separate

YouTube uses adaptive streaming (DASH) where video and audio are stored independently.
Combining them produces significantly higher quality than a single stream download.

---

## Planned Improvements

- Playlist downloads
- Resolution selector
- Merge progress tracking
- Pause and cancel support
- Executable build

---

## Disclaimer

This project is for educational purposes only.
Respect YouTube’s Terms of Service and copyright laws.
