import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from typing import Optional

class Branch(Base):
    __tablename__ = "branches"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id: Mapped[str] = mapped_column(String(36), ForeignKey("stories.id"))
    parent_checkpoint_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("checkpoints.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(100))
    
    # Directives for steering the LLM
    short_term_directive: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    long_term_directive: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
