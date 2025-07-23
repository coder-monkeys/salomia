import subprocess
from pathlib import Path
from .builder.py import build_ffmpeg_command
from .utils import validate_slides

def create_video(slides, output_path, audio=None, size="1080x1920"):
    """
    Create a slideshow video from images and text.

    :param slides: List of dicts, each like:
                   {"image": "path/to/img.jpg", "text": "Hello", "duration": 3}
    :param output_path: Path to save the output video.
    :param audio: Optional audio file for background music.
    :param size: Output resolution (default "1080x1920").
    """
    # Validate inputs
    validate_slides(slides)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Build ffmpeg command
    cmd = build_ffmpeg_command(slides, output_path, audio=audio, size=size)

    # Execute ffmpeg. 
    try:
        subprocess.run(cmd, check=True)
        print(f"Video created: {output_path}")
    except subprocess.CalledProcessError as e:
        print("Error while creating video:", e)
        raise
