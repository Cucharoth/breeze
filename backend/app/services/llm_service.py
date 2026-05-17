from typing import Any, Dict, List, Optional
from app.services.llm.interface import LLMProvider
from app.core.logger import logger
from app.core.prompt_manager import get_prompt, format_prompt

class LLMService:
    """
    Orchestrator service for LLM operations.
    Wraps a provider and adds high-level logic like prompt templating,
    retries, and feature-specific methods.
    """
    
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    @property
    def provider_name(self) -> str:
        return self.provider.provider_name

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        return await self.provider.generate(prompt, system_prompt=system_prompt)

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        return await self.provider.generate_json(prompt, system_prompt=system_prompt)

    async def generate_stream(self, prompt: str, system_prompt: Optional[str] = None) -> Any:
        async for token in self.provider.generate_stream(prompt, system_prompt=system_prompt):
            yield token

    async def generate_chat_stream(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> Any:
        async for token in self.provider.generate_chat_stream(messages, system_prompt=system_prompt):
            yield token

    async def generate_scenario(self, premise: str) -> Dict[str, Any]:
        """Specific orchestration for creating a new world scenario."""
        system_prompt = get_prompt("scenario_generator")
        prompt = format_prompt("scenario_premise", premise=premise)
        
        try:
            return await self.provider.generate_json(prompt, system_prompt=system_prompt)
        except Exception as e:
            logger.error(f"Scenario generation failed: {str(e)}")
            raise
