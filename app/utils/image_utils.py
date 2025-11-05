from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Tuple, Optional
import os


def load_image(image_path: str) -> Optional[Image.Image]:
    """
    Load an image from the given path.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        PIL Image object or None if loading fails
    """
    try:
        img = Image.open(image_path)
        return img.convert("RGB")
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None


def get_font(font_size: int) -> ImageFont.FreeTypeFont:
    """
    Get a font for text rendering. Tries to use Impact font (classic meme font),
    falls back to default if not available.
    
    Args:
        font_size: Size of the font
        
    Returns:
        ImageFont object
    """
    # Try common locations for Impact font
    impact_paths = [
        "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf",  # Linux
        "/System/Library/Fonts/Supplemental/Impact.ttf",  # macOS
        "C:\\Windows\\Fonts\\impact.ttf",  # Windows
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",  # Linux fallback
    ]
    
    for font_path in impact_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, font_size)
            except Exception:
                continue
    
    # Fall back to default font
    try:
        return ImageFont.truetype("arial.ttf", font_size)
    except Exception:
        return ImageFont.load_default()


def calculate_text_position(
    image_size: Tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    position: str = "top"
) -> Tuple[int, int]:
    """
    Calculate the position for text on the image.
    
    Args:
        image_size: (width, height) of the image
        text: Text to be rendered
        font: Font object
        position: "top" or "bottom"
        
    Returns:
        (x, y) coordinates for text placement
    """
    img_width, img_height = image_size
    
    # Create a temporary draw object to measure text
    temp_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(temp_img)
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center horizontally
    x = (img_width - text_width) // 2
    
    # Position vertically
    if position == "top":
        y = img_height * 0.05  # 5% from top
    else:  # bottom
        y = img_height * 0.95 - text_height  # 5% from bottom
    
    return int(x), int(y)


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """
    Wrap text to fit within a maximum width.
    
    Args:
        text: Text to wrap
        font: Font object
        max_width: Maximum width in pixels
        
    Returns:
        List of text lines
    """
    words = text.split()
    lines = []
    current_line = []
    
    # Create a temporary draw object to measure text
    temp_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(temp_img)
    
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]
        
        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    
    if current_line:
        lines.append(" ".join(current_line))
    
    return lines


def validate_image_file(file_path: str, max_size: int) -> Tuple[bool, str]:
    """
    Validate an image file.
    
    Args:
        file_path: Path to the image file
        max_size: Maximum file size in bytes
        
    Returns:
        (is_valid, error_message) tuple
    """
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        return False, "File does not exist"
    
    # Check file size
    if path.stat().st_size > max_size:
        return False, f"File size exceeds maximum of {max_size} bytes"
    
    # Try to open as image
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True, ""
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"
