import os
from pathlib import Path
from functools import lru_cache

PROMPTS_DIR = Path(__file__).parent.parent / "resources" / "prompts"

@lru_cache(maxsize=32)
def get_prompt(name: str, provider: str = "default") -> str:
    """
    Loads a prompt from the resources/prompts directory.
    Tries the provider-specific folder first, then falls back to default.
    Uses lru_cache to avoid repeated disk reads.
    """
    # Try provider specific first
    file_path = PROMPTS_DIR / provider / f"{name}.txt"
    if not file_path.exists():
        file_path = PROMPTS_DIR / provider / f"{name}.md"
        
    # Fallback to default
    if not file_path.exists():
        file_path = PROMPTS_DIR / "default" / f"{name}.txt"
    if not file_path.exists():
        file_path = PROMPTS_DIR / "default" / f"{name}.md"
        
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt template '{name}' not found for provider '{provider}' or 'default' in {PROMPTS_DIR}")
        
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def format_prompt(name: str, provider: str = "default", **kwargs) -> str:
    """
    Loads and formats a prompt with provided variables.
    """
    template = get_prompt(name, provider)
    return template.format(**kwargs)
