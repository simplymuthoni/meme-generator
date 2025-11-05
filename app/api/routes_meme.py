from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pathlib import Path

from app.models.meme_models import (
    MemeRequest,
    MemeResponse,
    ErrorResponse,
    AvailableTemplatesResponse
)
from app.services.meme_service import meme_service
from app.utils.ai_client import ai_client

router = APIRouter(prefix="/api/meme", tags=["meme"])


@router.post("/generate", response_model=MemeResponse)
async def generate_meme(request: MemeRequest, http_request: Request):
    """
    Generate a meme with the specified text and template.
    
    This endpoint can be called directly or triggered by an LLM using function calling.
    """
    try:
        # Generate the meme
        success, message, output_path = meme_service.generate_meme(
            template_name=request.template_name,
            top_text=request.top_text,
            bottom_text=request.bottom_text,
            font_size=request.font_size,
            font_color=request.font_color,
            stroke_color=request.stroke_color,
            stroke_width=request.stroke_width
        )
        
        if not success:
            raise HTTPException(status_code=400, detail=message)
        
        # Generate URL for the meme
        filename = Path(output_path).name
        base_url = str(http_request.base_url).rstrip("/")
        meme_url = f"{base_url}/static/memes/{filename}"
        
        return MemeResponse(
            success=True,
            message=message,
            meme_url=meme_url,
            filename=filename
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/templates", response_model=AvailableTemplatesResponse)
async def get_templates():
    """
    Get a list of all available meme templates.
    
    Returns the names of templates that can be used for meme generation.
    """
    try:
        templates = meme_service.get_available_templates()
        return AvailableTemplatesResponse(
            templates=templates,
            count=len(templates)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve templates: {str(e)}")


@router.post("/generate-with-ai")
async def generate_meme_with_ai(prompt: str, http_request: Request):
    """
    Generate a meme using AI to interpret the user's prompt.
    
    The AI will understand the prompt and call the appropriate meme generation function.
    
    Args:
        prompt: Natural language description of the meme to generate
        
    Example:
        "Create a distracted boyfriend meme about choosing Python over Java"
    """
    if not ai_client.is_configured():
        raise HTTPException(
            status_code=503,
            detail="AI service is not configured. Please set GOOGLE_API_KEY in environment variables."
        )
    
    try:
        # Generate response with function calling
        result = ai_client.generate_with_tools(prompt)
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to generate AI response")
        
        # Check if AI wants to call the meme generation function
        if result["function_calls"]:
            for func_call in result["function_calls"]:
                if func_call["name"] == "generate_meme":
                    # Extract arguments
                    args = func_call["args"]
                    
                    # Call the meme generation service
                    success, message, output_path = meme_service.generate_meme(
                        template_name=args.get("template_name"),
                        top_text=args.get("top_text"),
                        bottom_text=args.get("bottom_text"),
                        font_size=args.get("font_size", 40)
                    )
                    
                    if not success:
                        raise HTTPException(status_code=400, detail=message)
                    
                    # Generate URL
                    filename = Path(output_path).name
                    base_url = str(http_request.base_url).rstrip("/")
                    meme_url = f"{base_url}/static/memes/{filename}"
                    
                    return {
                        "success": True,
                        "message": message,
                        "meme_url": meme_url,
                        "filename": filename,
                        "ai_interpretation": result.get("text", "")
                    }
        
        # If no function was called, return the AI's text response
        return {
            "success": False,
            "message": "AI did not generate a meme",
            "ai_response": result.get("text", ""),
            "suggestion": "Try being more specific about the meme template and text you want."
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing AI request: {str(e)}")
