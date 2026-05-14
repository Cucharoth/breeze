from app.services.llm.base import LLMAdapter

class GeminiAdapter(LLMAdapter):
    async def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("GeminiAdapter not implemented yet")
