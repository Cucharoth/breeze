from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class BranchBase(BaseModel):
    name: str = Field(..., max_length=100)

class BranchCreate(BranchBase):
    pass

class BranchRead(BranchBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    story_id: int
    parent_checkpoint_id: Optional[int] = None
