from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    branch_id: int
    created_at: datetime
