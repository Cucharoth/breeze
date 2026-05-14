from pydantic import BaseModel, ConfigDict

class CheckpointBase(BaseModel):
    message_id: int

class CheckpointCreate(CheckpointBase):
    pass

class CheckpointRead(CheckpointBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    branch_id: int
