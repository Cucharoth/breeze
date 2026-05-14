from app.core.config import get_settings
from app.services.llm.ollama_adapter import OllamaAdapter

settings = get_settings()

def get_llm_adapter():
    """Dependency to provide the configured LLM adapter."""
    # For now, default to Ollama
    return OllamaAdapter(base_url=settings.OLLAMA_BASE_URL, model=settings.OLLAMA_MODEL)
