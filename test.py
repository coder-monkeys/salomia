import json

from core import create_video

with open("test.json", "r") as f:
    data = json.load(f)
create_video(
    template_json=data,
    output_path="output.mp4",
)
f.close()
