from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.branch import Branch
    from app.models.message import Message

class Checkpoint(Base):
    __tablename__ = "checkpoints"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"))
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"))
    
    # Relationships
    branch: Mapped["Branch"] = relationship("Branch", foreign_keys=[branch_id], back_populates="checkpoints")
    message: Mapped["Message"] = relationship("Message")
