from typing import Protocol, Any, Dict, List, Optional

class LLMProvider(Protocol):
    """
    Protocol defining the interface for LLM providers.
    Using Protocol (Structural Typing) allows for flexible implementations
    without rigid inheritance.
    """
    async def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """Generate a text response from a prompt."""
        ...

    async def generate_json(
        self, 
        prompt: str, 
        schema: Optional[Dict[str, Any]] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Generate a structured JSON response."""
        ...

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> Any: # AsyncIterator[str]
        """Generate a streaming text response."""
        ...
