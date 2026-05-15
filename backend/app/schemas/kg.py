from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class KGNodeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    branch_id: str
    name: str
    type: str
    description: Optional[str] = None

class KGEdgeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    branch_id: str
    source_node_id: str
    target_node_id: str
    relationship: str

class KGGraphRead(BaseModel):
    nodes: List[KGNodeRead]
    edges: List[KGEdgeRead]
