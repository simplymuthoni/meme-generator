"""
JSON Schema for LLM function/tool calling.
This allows Gemini/Gemma to autonomously call the meme generation API.
"""

MEME_GENERATOR_TOOL = {
    "name": "generate_meme",
    "description": "Generates a meme image by adding text to a meme template. Use this when the user wants to create a funny meme or add humorous captions to popular meme formats.",
    "parameters": {
        "type": "object",
        "properties": {
            "template_name": {
                "type": "string",
                "description": "The name of the meme template to use (e.g., 'distracted_boyfriend', 'drake', 'success_kid', 'one_does_not_simply')",
                "enum": [
                    "distracted_boyfriend",
                    "drake",
                    "success_kid",
                    "one_does_not_simply",
                    "change_my_mind",
                    "two_buttons",
                    "disaster_girl"
                ]
            },
            "top_text": {
                "type": "string",
                "description": "The text to display at the top of the meme. This is usually the setup or first part of the joke."
            },
            "bottom_text": {
                "type": "string",
                "description": "The text to display at the bottom of the meme. This is usually the punchline or second part of the joke. Optional for some meme formats."
            },
            "font_size": {
                "type": "integer",
                "description": "Font size for the text (default: 40, range: 10-200)",
                "minimum": 10,
                "maximum": 200,
                "default": 40
            }
        },
        "required": ["template_name", "top_text"]
    }
}


AVAILABLE_TEMPLATES_TOOL = {
    "name": "get_available_meme_templates",
    "description": "Returns a list of all available meme templates that can be used for meme generation.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}


# List of all tools for easy import
ALL_TOOLS = [
    MEME_GENERATOR_TOOL,
    AVAILABLE_TEMPLATES_TOOL
]
