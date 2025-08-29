import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from build_video import build_ffmpeg_command
from validation import validate_slides


def create_video(template_json: object, output_path: str) -> None:
    """
    Create a slideshow video from images and text.
    
    Args:
        template_json: List of dicts, each like:
               {"image": "path/to/img.jpg", "text": "Hello", "duration": 3}
        output_path: Path to save the output video.
    """
    # Validate inputs
    # validate_slides(template_json)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = build_ffmpeg_command(template_json, output_path)
    try:
        subprocess.run(cmd, check=True)
        add_looped_audio("output.mp4", "sample-9s.mp3", "output_w_audio.mp4")
        print(f"Video created: {output_path}")
    except subprocess.CalledProcessError as e:
        print("Error while creating video:", e)
        raise
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg and ensure it's in your PATH.")
        raise


def add_looped_audio(video_path, audio_path, output_path):
    """
    Loops audio until the video ends, replacing or mixing later.
    """
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-stream_loop", "-1", "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",  # stop at video length
        "-map", "0:v",  # video
        "-map", "1:a",  # audio
        output_path,
    ]
    subprocess.run(cmd, check=True)
