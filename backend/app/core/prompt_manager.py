import os
from pathlib import Path
from functools import lru_cache

PROMPTS_DIR = Path(__file__).parent.parent / "resources" / "prompts"

@lru_cache(maxsize=32)
def get_prompt(name: str) -> str:
    """
    Loads a prompt from the resources/prompts directory.
    Uses lru_cache to avoid repeated disk reads.
    """
    file_path = PROMPTS_DIR / f"{name}.txt"
    if not file_path.exists():
        # Fallback to .md if .txt doesn't exist
        file_path = PROMPTS_DIR / f"{name}.md"
        
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt template '{name}' not found in {PROMPTS_DIR}")
        
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def format_prompt(name: str, **kwargs) -> str:
    """
    Loads and formats a prompt with provided variables.
    """
    template = get_prompt(name)
    return template.format(**kwargs)
