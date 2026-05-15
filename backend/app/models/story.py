import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from typing import Optional

class Story(Base):
    __tablename__ = "stories"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scenario_id: Mapped[str] = mapped_column(String(36), ForeignKey("scenarios.id"))
    main_branch_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
