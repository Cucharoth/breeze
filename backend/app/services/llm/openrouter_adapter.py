from app.services.llm.base import LLMAdapter

class OpenRouterAdapter(LLMAdapter):
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("OpenRouterAdapter not implemented yet")
