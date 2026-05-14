from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class KGNodeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    branch_id: int
    name: str
    type: str
    description: Optional[str] = None

class KGEdgeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    branch_id: int
    source_node_id: int
    target_node_id: int
    relationship: str

class KGGraphRead(BaseModel):
    nodes: List[KGNodeRead]
    edges: List[KGEdgeRead]
