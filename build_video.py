from pathlib import Path
from typing import List, Dict, Any


def build_ffmpeg_command(template_json: Dict[str, Any], output_path: Path) -> List[str]:
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
    dimension_w = template_json['width']
    dimension_h = template_json['height']
    for i, slide in enumerate(images):
        text_attr = slide['attributes']['text'] if 'text' in slide['attributes'] else None
        inputs.extend(["-loop", "1", "-t", str(slide["duration"]), "-i", slide["image"]])
        filter_part_str = f"[{i}:v]scale={dimension_w}:{dimension_h},setsar=1,"
        if text_attr:
            text_position_x = text_attr['x']
            text_position_y = text_attr['y']
            safe_text = text_attr['content'].replace("'", r"\'").replace(':', r'\:')
            filter_part_str += f"drawtext=text='{safe_text}':fontcolor='{text_attr['fontcolor']}':fontsize={text_attr['fontsize']}:" \
                               f"x={text_position_x}:y={text_position_y}[slide{i}]"
        filter_parts.append(filter_part_str)
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
