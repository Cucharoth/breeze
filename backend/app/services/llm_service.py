from typing import Any, Dict, List, Optional
from app.services.llm.interface import LLMProvider
from app.core.logger import logger

class LLMService:
    """
    Orchestrator service for LLM operations.
    Wraps a provider and adds high-level logic like prompt templating,
    retries, and feature-specific methods.
    """
    
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        return await self.provider.generate(prompt, system_prompt=system_prompt)

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        return await self.provider.generate_json(prompt, system_prompt=system_prompt)

    async def generate_scenario(self, premise: str) -> Dict[str, Any]:
        """Specific orchestration for creating a new world scenario."""
        system_prompt = (
            "You are an expert world-builder and roleplay narrator. "
            "Given a premise, generate a rich world lore, a compelling first scene, "
            "and a list of key characters. Output must be strictly valid JSON."
        )
        
        prompt = f"""
        Generate a scenario based on this premise: {premise}
        
        Return a JSON object with:
        - world_lore: (string) Deep background and setting details.
        - first_scene: (string) The opening scene written in the 2nd person ('You...').
        - character_profiles: (list of objects) Each with 'name' and 'description'.
        """
        
        try:
            return await self.provider.generate_json(prompt, system_prompt=system_prompt)
        except Exception as e:
            logger.error(f"Scenario generation failed: {str(e)}")
            # Return a graceful fallback or re-raise
            raise
