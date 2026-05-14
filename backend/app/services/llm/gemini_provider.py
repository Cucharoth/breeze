import google.generativeai as genai
from typing import Any, Dict, Optional
from app.core.logger import logger

class GeminiProvider:
    """Native Google Gemini implementation of the LLMProvider protocol."""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    async def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        # Gemini usually combines system prompt into the first message or specialized config
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        try:
            response = await self.model.generate_content_async(full_prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation failed: {str(e)}")
            raise

    async def generate_json(
        self, 
        prompt: str, 
        schema: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        import json
        # Gemini 1.5 Pro/Flash support response_mime_type="application/json"
        # For now, we use a simple parsing approach
        text = await self.generate(prompt, system_prompt=system_prompt, **kwargs)
        return json.loads(text)
