import uuid
from sqlalchemy import String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    premise: Mapped[str] = mapped_column(String(500))
    world_lore: Mapped[str] = mapped_column(Text)
    first_scene: Mapped[str] = mapped_column(Text)
    character_profiles: Mapped[list] = mapped_column(JSON)  # List of dicts
