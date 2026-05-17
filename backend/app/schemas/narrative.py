from pydantic import BaseModel
from typing import Optional

class NextMessageRequest(BaseModel):
    speaker: Optional[str] = "the player"
