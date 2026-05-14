from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import List

class Story(Base):
    __tablename__ = "stories"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id"))
    
    # Relationships
    scenario = relationship("Scenario")
    branches: Mapped[List["Branch"]] = relationship("Branch", back_populates="story")
