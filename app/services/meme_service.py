from PIL import Image, ImageDraw
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple
import uuid

from app.config.settings import settings
from app.utils.image_utils import (
    load_image,
    get_font,
    calculate_text_position,
    wrap_text
)


class MemeService:
    """Service for generating memes using Pillow"""
    
    def __init__(self):
        """Initialize the meme service"""
        self.templates_dir = Path("app/static/templates")
        self.output_dir = settings.meme_output_path
        
        # Create directories if they don't exist
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_available_templates(self) -> list[str]:
        """
        Get list of available meme templates.
        
        Returns:
            List of template names (without extensions)
        """
        templates = []
        for file in self.templates_dir.glob("*"):
            if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif"]:
                templates.append(file.stem)
        return sorted(templates)
    
    def generate_meme(
        self,
        template_name: str,
        top_text: str,
        bottom_text: Optional[str] = None,
        font_size: int = None,
        font_color: str = None,
        stroke_color: str = None,
        stroke_width: int = None
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Generate a meme with text overlay.
        
        Args:
            template_name: Name of the template image
            top_text: Text for the top of the image
            bottom_text: Text for the bottom of the image (optional)
            font_size: Size of the font
            font_color: Color of the text
            stroke_color: Color of the text outline
            stroke_width: Width of the text outline
            
        Returns:
            (success, message, output_path) tuple
        """
        # Use defaults from settings if not provided
        font_size = font_size or settings.default_font_size
        font_color = font_color or settings.default_font_color
        stroke_color = stroke_color or settings.default_stroke_color
        stroke_width = stroke_width or settings.default_stroke_width
        
        # Find template file
        template_path = self._find_template(template_name)
        if not template_path:
            return False, f"Template '{template_name}' not found", None
        
        # Load the image
        img = load_image(str(template_path))
        if not img:
            return False, "Failed to load template image", None
        
        # Create a draw object
        draw = ImageDraw.Draw(img)
        
        # Get font
        font = get_font(font_size)
        
        # Add top text
        if top_text:
            self._add_text_to_image(
                draw,
                img.size,
                top_text,
                font,
                font_color,
                stroke_color,
                stroke_width,
                position="top"
            )
        
        # Add bottom text if provided
        if bottom_text:
            self._add_text_to_image(
                draw,
                img.size,
                bottom_text,
                font,
                font_color,
                stroke_color,
                stroke_width,
                position="bottom"
            )
        
        # Generate unique filename
        filename = self._generate_filename(template_name)
        output_path = self.output_dir / filename
        
        # Save the meme
        try:
            img.save(output_path, quality=95)
            return True, "Meme generated successfully", str(output_path)
        except Exception as e:
            return False, f"Failed to save meme: {str(e)}", None
    
    def _find_template(self, template_name: str) -> Optional[Path]:
        """Find a template file by name"""
        for ext in [".jpg", ".jpeg", ".png", ".gif"]:
            template_path = self.templates_dir / f"{template_name}{ext}"
            if template_path.exists():
                return template_path
        return None
    
    def _add_text_to_image(
        self,
        draw: ImageDraw.ImageDraw,
        image_size: Tuple[int, int],
        text: str,
        font,
        font_color: str,
        stroke_color: str,
        stroke_width: int,
        position: str
    ):
        """Add text to the image with outline"""
        img_width, img_height = image_size
        
        # Wrap text if it's too long
        max_width = int(img_width * 0.9)  # Use 90% of image width
        lines = wrap_text(text.upper(), font, max_width)
        
        # Calculate total text height
        temp_img = Image.new("RGB", (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        line_height = temp_draw.textbbox((0, 0), "A", font=font)[3]
        total_height = line_height * len(lines)
        
        # Calculate starting Y position
        if position == "top":
            y_start = int(img_height * 0.05)
        else:  # bottom
            y_start = int(img_height * 0.95 - total_height)
        
        # Draw each line
        for i, line in enumerate(lines):
            # Calculate position for this line
            bbox = temp_draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (img_width - text_width) // 2
            y = y_start + (i * line_height)
            
            # Draw text with outline (stroke)
            draw.text(
                (x, y),
                line,
                font=font,
                fill=font_color,
                stroke_width=stroke_width,
                stroke_fill=stroke_color
            )
    
    def _generate_filename(self, template_name: str) -> str:
        """Generate a unique filename for the meme"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"{template_name}_{timestamp}_{unique_id}.jpg"


# Global meme service instance
meme_service = MemeService()
