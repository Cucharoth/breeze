from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class BranchBase(BaseModel):
    story_id: str
    name: str = Field(..., max_length=100)
    short_term_directive: Optional[str] = Field(None, max_length=500)
    long_term_directive: Optional[str] = Field(None, max_length=1000)

class BranchCreate(BranchBase):
    pass

class BranchRead(BranchBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    parent_checkpoint_id: Optional[str] = None
