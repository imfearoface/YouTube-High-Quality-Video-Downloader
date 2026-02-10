🎬 YouTube Video Downloader & Merger (Python + FFmpeg)

This project downloads the highest-quality video and audio streams from a YouTube video and merges them into a single MP4 file using FFmpeg.

It uses the pytubefix library to access adaptive streams and automatically generates safe filenames based on the video title.

🚀 Features

Downloads highest available video quality

Downloads highest available audio quality

Merges video and audio into one MP4 file

Cleans video titles for valid filenames

Automatically deletes temporary files

Simple GUI with progress bars

📦 Requirements

Python 3.8 or higher

FFmpeg

pytubefix

📥 Installation

Install pytubefix:

pip install pytubefix


Download FFmpeg:
https://ffmpeg.org/download.html

⚙️ Setup

Edit the script and update:

🎥 Video URL (if using CLI mode)
video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

🧰 FFmpeg Path (Windows example)
ffmpeg_path = r"Z:\your_path\ffmpeg.exe"

▶️ Usage

Run the script:

python YoutubeDownloader.py


Example output:

Saved file:
C:\Videos\My Video Title.mp4

🧠 How It Works

Retrieves highest-resolution video stream

Retrieves highest-bitrate audio stream

Downloads streams separately

Merges with FFmpeg

Deletes temporary files

Saves final MP4

📌 Why Separate Video & Audio?

YouTube delivers high-quality content using adaptive streaming (DASH), where video and audio are stored separately. Merging them produces significantly better quality.

🚧 Future Improvements

Playlist downloading

Resolution selector

Merge progress bar

Cancel / pause support

Export as .exe

⚠️ Disclaimer

This project is for educational purposes only.
Always respect YouTube’s Terms of Service and copyright laws.
