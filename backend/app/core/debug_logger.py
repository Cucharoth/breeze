import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from app.core.logger import logger

DEBUG_DIR = Path("debug/prompts")
MAX_LOG_FILES = 5

def ensure_debug_dir():
    """Ensure the debug directory exists and rotate old logs."""
    if not DEBUG_DIR.exists():
        DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Prune old logs
    logs = sorted(DEBUG_DIR.glob("*.md"), key=lambda x: x.stat().st_mtime)
    if len(logs) > MAX_LOG_FILES:
        for i in range(len(logs) - MAX_LOG_FILES):
            try:
                logs[i].unlink()
            except Exception as e:
                logger.warning(f"Failed to delete old log {logs[i]}: {e}")

async def log_llm_interaction(branch_id: str, system_prompt: str, prompt: str, response: str):
    """
    Logs an LLM interaction to a Markdown file with both formatted and raw views.
    """
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _perform_log, branch_id, system_prompt, prompt, response)
    except Exception as e:
        logger.error(f"Failed to log LLM interaction: {str(e)}")

def _perform_log(branch_id: str, system_prompt: str, prompt: str, response: str):
    ensure_debug_dir()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{timestamp}_{branch_id[:8]}.md"
    file_path = DEBUG_DIR / filename
    
    # Format the Markdown content
    md_content = f"""# LLM Interaction Log
**Branch ID:** `{branch_id}`
**Timestamp:** `{datetime.now().isoformat()}`

---

## ⚙️ System Prompt (Formatted)
> {system_prompt.replace('\n', '\n> ')}

---

## 📜 Conversation History (Readable)
{_format_history(prompt)}

---

## 🛠️ Technical Trace (Raw Payload)
This is exactly what was sent to the model:
```text
{prompt}
```

---

## 🤖 Model Response
{response}

---

## 🧱 Raw Response
```text
{response}
```
"""
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    logger.debug(f"Detailed prompt log written to {file_path}")

def _format_history(prompt: str) -> str:
    """Makes the raw prompt history readable for Markdown."""
    # Split by common role patterns we use
    lines = prompt.split("\n\n")
    formatted = []
    
    for line in lines:
        if line.startswith("Narrator:"):
            formatted.append(f"### 🖋️ Narrator\n{line.replace('Narrator:', '').strip()}")
        elif line.startswith("User:"):
             formatted.append(f"### 👤 User\n{line.replace('User:', '').strip()}")
        elif line.startswith("Assistant:"):
             formatted.append(f"### 🤖 Assistant\n{line.replace('Assistant:', '').strip()}")
        elif line.startswith("("):
             formatted.append(f"**Constraint:** *{line.strip()}*")
        else:
             formatted.append(line.strip())
             
    return "\n\n".join(formatted)
