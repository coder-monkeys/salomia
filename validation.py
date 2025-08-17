from typing import Dict, List
from pathlib import Path



def validate_slides(slides: List[Dict]) -> None:
    """Validate the slides input."""
    if not slides:
        raise ValueError("At least one slide is required")
    
    for slide in slides:
        if not isinstance(slide, dict):
            raise ValueError("Each slide must be a dictionary")
        
        if "image" not in slide:
            raise ValueError("Each slide must have an 'image' key")
        
        if not Path(slide["image"]).exists():
            raise ValueError(f"Image file not found: {slide['image']}")
        
        if "duration" not in slide:
            slide["duration"] = 5  # Default duration if not provided
