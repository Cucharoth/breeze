from app.core.config import get_settings
from app.services.llm.ollama_provider import OllamaProvider
from app.services.llm_service import LLMService

settings = get_settings()

def get_llm_service() -> LLMService:
    """
    Dependency to provide the configured LLM service.
    This is the central place to swap providers or change configuration.
    """
    # For now, we default to Ollama as the provider
    provider = OllamaProvider(
        base_url=settings.OLLAMA_BASE_URL, 
        model=settings.OLLAMA_MODEL
    )
    
    return LLMService(provider=provider)
