from pydantic import BaseModel, ConfigDict
from typing import Optional

class StoryBase(BaseModel):
    scenario_id: int

class StoryCreate(StoryBase):
    pass

class StoryRead(StoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    main_branch_id: Optional[int] = None
