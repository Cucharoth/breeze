from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.story import Story
    from app.models.message import Message
    from app.models.checkpoint import Checkpoint

class Branch(Base):
    __tablename__ = "branches"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    story_id: Mapped[int] = mapped_column(ForeignKey("stories.id"))
    parent_checkpoint_id: Mapped[Optional[int]] = mapped_column(ForeignKey("checkpoints.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(100), default="Main Branch")
    
    # Relationships
    story: Mapped["Story"] = relationship("Story", back_populates="branches")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="branch")
    checkpoints: Mapped[List["Checkpoint"]] = relationship("Checkpoint", foreign_keys="[Checkpoint.branch_id]", back_populates="branch")
