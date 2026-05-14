from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any

class ScenarioBase(BaseModel):
    premise: str = Field(..., max_length=500)

class ScenarioCreate(ScenarioBase):
    pass

class ScenarioRead(ScenarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    world_lore: str
    first_scene: str
    character_profiles: List[Dict[str, Any]]
