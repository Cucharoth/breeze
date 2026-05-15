from pydantic import BaseModel, ConfigDict
from typing import Optional

class StoryBase(BaseModel):
    scenario_id: str

class StoryCreate(StoryBase):
    pass

class StoryRead(StoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    main_branch_id: Optional[str] = None

class BranchTreeNode(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    parent_checkpoint_id: Optional[str] = None

class CheckpointTreeNode(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    branch_id: str
    message_id: str

class StoryTreeRead(BaseModel):
    story_id: str
    scenario_id: str
    branches: list[BranchTreeNode]
    checkpoints: list[CheckpointTreeNode]
