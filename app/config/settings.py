from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Settings
    app_name: str = "Meme Generator API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Google AI Settings
    google_api_key: str = ""
    
    # Meme Generation Settings
    meme_output_dir: str = "app/static/memes"
    max_image_size: int = 10485760  # 10MB
    allowed_extensions: List[str] = ["jpg", "jpeg", "png", "gif"]
    
    # Font Settings
    default_font_size: int = 40
    default_font_color: str = "white"
    default_stroke_color: str = "black"
    default_stroke_width: int = 2
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def meme_output_path(self) -> Path:
        """Get the meme output directory as a Path object"""
        path = Path(self.meme_output_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path


# Global settings instance
settings = Settings()