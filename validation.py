from typing import Dict, List
from pathlib import Path


def validate_slides(template_json: object) -> None:
    """Validate the slides input."""
    if not template_json:
        raise ValueError("At least one slide is required")

    if "image" not in template_json:
        raise ValueError("Each slide must have an 'image' key")
