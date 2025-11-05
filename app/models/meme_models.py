from pydantic import BaseModel, Field
from typing import Optional, Literal


class MemeRequest(BaseModel):
    """Request model for meme generation"""
    
    template_name: str = Field(
        ...,
        description="Name of the meme template (e.g., 'distracted_boyfriend', 'drake')",
        examples=["distracted_boyfriend"]
    )
    top_text: str = Field(
        ...,
        description="Text to display at the top of the meme",
        examples=["When you see a bug in production"]
    )
    bottom_text: Optional[str] = Field(
        None,
        description="Text to display at the bottom of the meme",
        examples=["But it's Friday at 5pm"]
    )
    font_size: Optional[int] = Field(
        40,
        ge=10,
        le=200,
        description="Font size for the text"
    )
    font_color: Optional[str] = Field(
        "white",
        description="Color of the text (name or hex)"
    )
    stroke_color: Optional[str] = Field(
        "black",
        description="Color of the text outline"
    )
    stroke_width: Optional[int] = Field(
        2,
        ge=0,
        le=10,
        description="Width of the text outline"
    )


class MemeResponse(BaseModel):
    """Response model after successful meme generation"""
    
    success: bool = Field(..., description="Whether the meme was generated successfully")
    message: str = Field(..., description="Status message")
    meme_url: Optional[str] = Field(None, description="URL to access the generated meme")
    filename: Optional[str] = Field(None, description="Filename of the generated meme")


class ErrorResponse(BaseModel):
    """Error response model"""
    
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")


class AvailableTemplatesResponse(BaseModel):
    """Response model for available templates"""
    
    templates: list[str] = Field(..., description="List of available meme templates")
    count: int = Field(..., description="Number of available templates")
