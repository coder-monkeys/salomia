from pathlib import Path
from typing import Dict, List, Optional


def build_ffmpeg_command(slides: List[Dict], output_path: Path,
                         audio: Optional[str] = None, size: str = "1080x1920") -> List[str]:
    """
    Build the ffmpeg command for creating a slideshow video.
    
    Args:
        slides: List of slide dictionaries
        output_path: Output video file path
        audio: Optional audio file path
        size: Video resolution (format: WxH)
    
    Returns:
        List of command arguments for subprocess
    """
    inputs = []
    filter_parts = []
    for i, slide in enumerate(slides):
        inputs.extend(["-loop", "1", "-t", str(slide["duration"]), "-i", slide["image"]])
        width = int(slide['width'])
        height = int(slide['height'])
        print(width, height)
        safe_text = slide['text'].replace("'", r"\'").replace(':', r'\:')

        filter_parts.append(
            f"[{i}:v]scale=1080:1350,setsar=1,"
            f"drawtext=text='{safe_text}':fontcolor='{slide['fontcolor']}':fontsize={slide['fontsize']}:"
            f"x=(w-text_w)/2:y=h-100[slide{i}]"
        )

    concat_inputs = "".join(f"[slide{i}]" for i in range(len(slides)))
    filter_complex = ";".join(filter_parts) + f";{concat_inputs}concat=n={len(slides)}:v=1:a=0[outv]"

    cmd = [
        "ffmpeg",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "output.mp4"
    ]

    print("Running command:", " ".join(cmd))
    return cmd
