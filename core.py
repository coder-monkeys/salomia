import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from build_video import build_ffmpeg_command
from validation import validate_slides


def create_video(slides: List[Dict], output_path: str,
                 audio: Optional[str] = None, size: str = "1080x1920") -> None:
    """
    Create a slideshow video from images and text.
    
    Args:
        slides: List of dicts, each like:
               {"image": "path/to/img.jpg", "text": "Hello", "duration": 3}
        output_path: Path to save the output video.
        audio: Optional audio file for background music.
        size: Output resolution (default "1080x1920").
    """
    # Validate inputs
    validate_slides(slides)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = build_ffmpeg_command(slides, output_path, audio=audio, size=size)
    try:
        subprocess.run(cmd, check=True)
        print(f"Video created: {output_path}")
    except subprocess.CalledProcessError as e:
        print("Error while creating video:", e)
        raise
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg and ensure it's in your PATH.")
        raise
