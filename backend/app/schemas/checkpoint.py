from pydantic import BaseModel, ConfigDict

class CheckpointBase(BaseModel):
    message_id: str

class CheckpointCreate(CheckpointBase):
    pass

class CheckpointRead(CheckpointBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    branch_id: str
