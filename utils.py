# video_slideshow/utils.py
import os

DEFAULT_FONT_SIZE = 40
DEFAULT_FONT_COLOR = "white"
DEFAULT_BOX_COLOR = "black"
DEFAULT_BOX_ALPHA = 0.5
DEFAULT_DURATION = 3  # seconds

def validate_slides(slides):
    """
    Validates and sets defaults for slides.
    Each slide must be a dict with at least 'image'.
    """
    if not isinstance(slides, list):
        raise ValueError("Slides must be a list of dictionaries.")

    for idx, slide in enumerate(slides):
        if not isinstance(slide, dict):
            raise ValueError(f"Slide {idx} must be a dictionary.")

        # Check image
        image = slide.get("image")
        if not image:
            raise ValueError(f"Slide {idx} is missing the 'image' key.")
        if not os.path.isfile(image):
            raise FileNotFoundError(f"Image file not found: {image}")

        # Set default values if missing
        slide.setdefault("text", "")
        slide.setdefault("duration", DEFAULT_DURATION)
        slide.setdefault("fontsize", DEFAULT_FONT_SIZE)
        slide.setdefault("fontcolor", DEFAULT_FONT_COLOR)
        slide.setdefault("boxcolor", DEFAULT_BOX_COLOR)
        slide.setdefault("boxalpha", DEFAULT_BOX_ALPHA)

        # Validate duration
        try:
            slide["duration"] = float(slide["duration"])
            if slide["duration"] <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError(f"Invalid duration for slide {idx}: {slide['duration']}")

    return slides

def ensure_dir(path):
    """
    Ensures that the directory for the given path exists.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

def escape_text(text):
    """
    Escapes text for safe use in FFmpeg drawtext.
    """
    return text.replace(":", r'\:').replace("'", r"\'")
