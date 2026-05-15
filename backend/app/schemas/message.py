from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    branch_id: str
    created_at: datetime
