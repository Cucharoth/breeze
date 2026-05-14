import httpx
from typing import Any, Dict, Optional
from app.core.logger import logger

class OpenRouterProvider:
    """OpenRouter implementation of the LLMProvider protocol."""
    
    def __init__(self, api_key: str, model: str = "google/gemini-pro-1.5"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    async def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://breeze-rp.com", # Required by OpenRouter
            "X-Title": "Breeze-RP"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            **kwargs
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.base_url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"OpenRouter generation failed: {str(e)}")
                raise

    async def generate_json(
        self, 
        prompt: str, 
        schema: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        # Simple implementation for now, might need better prompting
        import json
        text = await self.generate(prompt, system_prompt=system_prompt, **kwargs)
        return json.loads(text)
