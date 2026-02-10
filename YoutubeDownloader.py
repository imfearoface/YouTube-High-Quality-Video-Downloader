from pytubefix import YouTube
import os
import subprocess
import re
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk

# YouTube URL validation

YOUTUBE_PATTERN = re.compile(
    r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+"
)

def sanitize_title(title: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", title).strip()


# GUI App

def main():
    ffmpeg_path = r"Z:\PyTube Scripts\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"
    output_dir = {"path": os.getcwd()}  # mutable container

    itag_to_kind = {}
    filesize_by_itag = {}

    root = tk.Tk()
    root.title("YouTube Downloader")
    root.geometry("740x420")
    root.resizable(False, False)

    # --- URL input ---
    tk.Label(root, text="Enter the YouTube video URL:").pack(pady=(15, 5))

    entry = tk.Entry(root, width=95)
    entry.pack(pady=5)
    entry.focus_set()

    # --- Output folder ---
    folder_frame = tk.Frame(root)
    folder_frame.pack(pady=(10, 0))

    tk.Label(folder_frame, text="Save to:").grid(row=0, column=0, sticky="w")

    folder_label = tk.Label(folder_frame, text=output_dir["path"], width=62, anchor="w")
    folder_label.grid(row=0, column=1, padx=(10, 10))

    def choose_folder():
        chosen = filedialog.askdirectory()
        if chosen:
            output_dir["path"] = chosen
            folder_label.config(text=chosen)

    tk.Button(folder_frame, text="Choose Folder", command=choose_folder).grid(row=0, column=2)

    # --- Status ---
    status_var = tk.StringVar(value="Status: Waiting for URL...")
    tk.Label(root, textvariable=status_var).pack(pady=(12, 0))

    # --- Progress UI ---
    prog_frame = tk.Frame(root)
    prog_frame.pack(pady=(18, 0), fill="x")

    tk.Label(prog_frame, text="Video Download:").grid(row=0, column=0, sticky="w", padx=10)
    video_bar = ttk.Progressbar(prog_frame, orient="horizontal", length=520, mode="determinate", maximum=100)
    video_bar.grid(row=0, column=1, padx=10)
    video_pct = tk.StringVar(value="0%")
    tk.Label(prog_frame, textvariable=video_pct, width=5).grid(row=0, column=2, padx=(0, 10))

    tk.Label(prog_frame, text="Audio Download:").grid(row=1, column=0, sticky="w", padx=10, pady=(12, 0))
    audio_bar = ttk.Progressbar(prog_frame, orient="horizontal", length=520, mode="determinate", maximum=100)
    audio_bar.grid(row=1, column=1, padx=10, pady=(12, 0))
    audio_pct = tk.StringVar(value="0%")
    tk.Label(prog_frame, textvariable=audio_pct, width=5).grid(row=1, column=2, padx=(0, 10), pady=(12, 0))

    # --- Saved output path display ---
    saved_var = tk.StringVar(value="")
    tk.Label(root, textvariable=saved_var, wraplength=700, fg="green").pack(pady=(20, 0))

    def set_status(msg: str):
        status_var.set(f"Status: {msg}")
        root.update_idletasks()

    def reset_progress():
        video_bar["value"] = 0
        audio_bar["value"] = 0
        video_pct.set("0%")
        audio_pct.set("0%")
        root.update_idletasks()

    # Progress callback (called during downloads)
    
    def on_progress(stream, chunk, bytes_remaining):
        itag = getattr(stream, "itag", None)
        if itag is None:
            return

        kind = itag_to_kind.get(itag)
        total = filesize_by_itag.get(itag)

        if not kind or not total:
            return

        downloaded = total - bytes_remaining
        pct = max(0, min(100, int(downloaded * 100 / total)))

        def update_ui():
            if kind == "video":
                video_bar["value"] = pct
                video_pct.set(f"{pct}%")
            elif kind == "audio":
                audio_bar["value"] = pct
                audio_pct.set(f"{pct}%")

        # Schedule UI update on main thread
        root.after(0, update_ui)

    # Worker (runs in background thread)

    def worker_download(url: str):
        try:
            set_status("Preparing streams...")

            yt = YouTube(url, on_progress_callback=on_progress)

            video_stream = (
                yt.streams
                .filter(adaptive=True, file_extension="mp4", only_video=True)
                .order_by("resolution")
                .desc()
                .first()
            )

            audio_stream = (
                yt.streams
                .filter(adaptive=True, file_extension="mp4", only_audio=True)
                .order_by("abr")
                .desc()
                .first()
            )

            if not video_stream or not audio_stream:
                raise RuntimeError("Could not find suitable video/audio streams for this URL.")

            # Map itags -> which progress bar to update
            itag_to_kind.clear()
            filesize_by_itag.clear()

            itag_to_kind[video_stream.itag] = "video"
            itag_to_kind[audio_stream.itag] = "audio"

            # Some streams expose filesize; fallback to filesize_approx if needed
            v_size = getattr(video_stream, "filesize", None) or getattr(video_stream, "filesize_approx", None)
            a_size = getattr(audio_stream, "filesize", None) or getattr(audio_stream, "filesize_approx", None)

            if not v_size or not a_size:
                # If filesize isn't available, switch to indeterminate (rare case)
                root.after(0, lambda: set_status("Filesize unknown; progress may be limited."))

            filesize_by_itag[video_stream.itag] = int(v_size) if v_size else 1
            filesize_by_itag[audio_stream.itag] = int(a_size) if a_size else 1

            # Temp files in output folder
            out_dir = output_dir["path"]
            temp_video = os.path.join(out_dir, "temp_video.mp4")
            temp_audio = os.path.join(out_dir, "temp_audio.mp4")

            safe_title = sanitize_title(yt.title)
            output_file = os.path.join(out_dir, f"{safe_title}.mp4")

            # Download video
            set_status("Downloading video...")
            video_stream.download(output_path=out_dir, filename="temp_video.mp4")

            # Download audio
            set_status("Downloading audio...")
            audio_stream.download(output_path=out_dir, filename="temp_audio.mp4")

            # Merge
            set_status("Merging with FFmpeg...")
            result = subprocess.run([
                ffmpeg_path, "-y",
                "-i", temp_video, "-i", temp_audio,
                "-c:v", "copy", "-c:a", "aac",
                output_file
            ], capture_output=True, text=True)

            # Cleanup temp files
            if os.path.exists(temp_video):
                os.remove(temp_video)
            if os.path.exists(temp_audio):
                os.remove(temp_audio)

            if result.returncode != 0:
                raise RuntimeError(f"FFmpeg merge failed:\n{result.stderr}")

            saved_path = os.path.abspath(output_file)
            root.after(0, lambda: saved_var.set(f"Saved file:\n{saved_path}"))
            set_status("Completed successfully")

        except Exception as e:
            err_msg = str(e)
            set_status("Error")
            root.after(0, lambda msg=err_msg: messagebox.showerror("Download Failed", msg))

        finally:
            root.after(0, lambda: download_btn.config(state="normal"))


    # Submit button handler

    def submit():
        url = entry.get().strip()

        if not YOUTUBE_PATTERN.match(url):
            messagebox.showerror(
                "Invalid URL",
                "Please enter a valid YouTube URL.\n\nExamples:\n- https://www.youtube.com/watch?v=...\n- https://youtu.be/..."
            )
            entry.focus_set()
            entry.selection_range(0, tk.END)
            return

        if not os.path.exists(ffmpeg_path):
            messagebox.showerror("FFmpeg Not Found", f"FFmpeg path does not exist:\n{ffmpeg_path}")
            return

        download_btn.config(state="disabled")
        saved_var.set("")
        reset_progress()
        set_status("Starting...")

        # Run download in background so GUI stays responsive
        t = threading.Thread(target=worker_download, args=(url,), daemon=True)
        t.start()

    entry.bind("<Return>", lambda e: submit())

    download_btn = tk.Button(root, text="Download", command=submit)
    download_btn.pack(pady=16)

    root.mainloop()

if __name__ == "__main__":
    main()
