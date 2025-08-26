from core import create_video

slides = [
    {
        "image": "slide1.jpg",
        "text": "Welcome to my video",
        "duration": 5,
        "fontsize": 50,
        "fontcolor": "#FF5733"
    },
    {
        "image": "slide2.jpg",
        "text": "Another message here",
        "duration": 3,
        "fontsize": 30,
        "fontcolor": "#FF5733"
    },
]

create_video(
    slides=slides,
    output_path="output.mp4",
    audio="background_music.mp3",
    size="1080x1920"
)
