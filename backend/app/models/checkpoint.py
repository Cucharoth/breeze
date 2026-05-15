import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Checkpoint(Base):
    __tablename__ = "checkpoints"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    branch_id: Mapped[str] = mapped_column(String(36), ForeignKey("branches.id"))
    message_id: Mapped[str] = mapped_column(String(36), ForeignKey("messages.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
