import google.generativeai as genai
from app.config.settings import settings
from app.models.tool_schema import ALL_TOOLS
from typing import Optional, Dict, Any


class AIClient:
    """Wrapper for Google Generative AI (Gemini/Gemma) client"""
    
    def __init__(self):
        """Initialize the AI client with API key from settings"""
        if settings.google_api_key:
            genai.configure(api_key=settings.google_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def is_configured(self) -> bool:
        """Check if the AI client is properly configured"""
        return self.model is not None
    
    def generate_with_tools(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Generate a response with function calling capabilities.
        
        Args:
            prompt: User prompt
            
        Returns:
            Dictionary containing the response and any tool calls
        """
        if not self.is_configured():
            return None
        
        try:
            # Convert our tool schema to Gemini format
            tools = self._convert_tools_to_gemini_format()
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                tools=tools
            )
            
            # Parse response for function calls
            result = {
                "text": response.text if hasattr(response, 'text') else "",
                "function_calls": []
            }
            
            # Check if model wants to call a function
            if hasattr(response, 'candidates') and response.candidates:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call'):
                        func_call = part.function_call
                        result["function_calls"].append({
                            "name": func_call.name,
                            "args": dict(func_call.args)
                        })
            
            return result
            
        except Exception as e:
            print(f"Error generating with tools: {e}")
            return None
    
    def _convert_tools_to_gemini_format(self) -> list:
        """Convert our tool schema to Gemini's expected format"""
        gemini_tools = []
        
        for tool in ALL_TOOLS:
            gemini_tool = {
                "function_declarations": [{
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }]
            }
            gemini_tools.append(gemini_tool)
        
        return gemini_tools
    
    def simple_generate(self, prompt: str) -> Optional[str]:
        """
        Generate a simple text response without tools.
        
        Args:
            prompt: User prompt
            
        Returns:
            Generated text response
        """
        if not self.is_configured():
            return None
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return None


# Global AI client instance
ai_client = AIClient()
