import httpx
import json
from typing import Any, Dict, Optional, List
from app.core.logger import logger

class OllamaProvider:
    """Ollama implementation of the LLMProvider protocol."""
    
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = httpx.Timeout(120.0, connect=10.0)

    async def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            **kwargs
        }
        if system_prompt:
            payload["system"] = system_prompt

        logger.debug(f"Ollama: Sending request to {url} with model {self.model}")
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                result = response.json().get("response", "")
                logger.debug(f"Ollama: Generation successful ({len(result)} chars)")
                return result
            except Exception as e:
                logger.error(f"Ollama generation failed: {str(e)}")
                raise

    async def generate_json(
        self, 
        prompt: str, 
        schema: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        # Ollama supports format="json"
        response_text = await self.generate(
            prompt, 
            system_prompt=system_prompt, 
            format="json", 
            **kwargs
        )
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode Ollama JSON response: {response_text}")
            raise ValueError(f"Invalid JSON from LLM: {str(e)}")

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> Any: # AsyncIterator[str]
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            **kwargs
        }
        if system_prompt:
            payload["system"] = system_prompt

        logger.debug(f"Ollama Stream: Starting request to {url}")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream("POST", url, json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        token = data.get("response", "")
                        if token:
                            yield token
                        if data.get("done"):
                            break
                    except json.JSONDecodeError:
                        continue
