# YouTube-High-Quality-Video-Downloader
YouTube High-Quality Video Downloader with Audio Merge

from pytubefix import YouTube
import os
import subprocess
import re

# Insert Video URL
video_url = "(https://www.youtube.com/watch?v=K-OkvetOmBE)"

# Variables
yt = YouTube(video_url)
video_stream = yt.streams.filter(adaptive=True, file_extension="mp4", only_video=True).order_by("resolution").desc().first()
audio_stream = yt.streams.filter(adaptive=True, file_extension="mp4", only_audio=True).order_by("abr").desc().first()
video_file = "video.mp4"
audio_file = "audio.mp4"

# Clean title for filename
safe_title = re.sub(r'[\\/*?:"<>|]', "", yt.title)
output_file = f"{safe_title}.mp4"

# Download streams
video_stream.download(filename=video_file)
audio_stream.download(filename=audio_file)

ffmpeg_path = r"Z:\PyTube Scripts\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"

# Merge
subprocess.run([
    ffmpeg_path, "-i", video_file, "-i", audio_file,
    "-c:v", "copy", "-c:a", "aac", "-strict", "experimental",
    output_file
])

os.remove(video_file)
os.remove(audio_file)

print(f"Saved as: {output_file}")
