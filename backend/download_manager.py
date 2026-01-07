import yt_dlp
import os
import uuid

def download_video(url: str, download_dir: str = "temp_downloads") -> str:
    """
    Downloads a video from the given URL using yt-dlp.
    Returns the absolute path to the downloaded file.
    """
    if not url.strip().lower().startswith(("http://", "https://")):
        raise ValueError("Invalid URL: Must start with http:// or https://")

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Generate a unique filename to avoid collisions
    unique_id = str(uuid.uuid4())
    output_template = os.path.join(download_dir, f"{unique_id}.mp4")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_template,
        'merge_output_format': 'mp4', # Force merge to mp4
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
    return os.path.abspath(filename)
