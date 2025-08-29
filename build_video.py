from pathlib import Path
from typing import List


def build_ffmpeg_command(template_json: object, output_path: Path) -> List[str]:
    """
    Build the ffmpeg command for creating a slideshow video.
    Args:
        template_json: List of slide dictionaries
        output_path: Output video file path
    Returns:
        List of command arguments for subprocess
    """
    inputs = []
    filter_parts = []
    images = template_json['images']
    videos = template_json['videos']
    audio_path = template_json['audio']
    for i, slide in enumerate(images):
        inputs.extend(["-loop", "1", "-t", str(slide["duration"]), "-i", slide["image"]])
        safe_text = slide['text'].replace("'", r"\'").replace(':', r'\:')

        filter_parts.append(
            f"[{i}:v]scale=1080:1350,setsar=1,"
            f"drawtext=text='{safe_text}':fontcolor='{slide['fontcolor']}':fontsize={slide['fontsize']}:"
            f"x=(w-text_w)/2:y=h-100[slide{i}]"
        )

    concat_inputs = "".join(f"[slide{i}]" for i in range(len(images)))
    filter_complex = ";".join(filter_parts) + f";{concat_inputs}concat=n={len(images)}:v=1:a=0[outv]"

    cmd = [
        "ffmpeg",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        str(output_path)
    ]

    print("Running command:", " ".join(cmd))
    return cmd
