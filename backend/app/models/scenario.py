from sqlalchemy import String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    premise: Mapped[str] = mapped_column(String(500))
    world_lore: Mapped[str] = mapped_column(Text)
    first_scene: Mapped[str] = mapped_column(Text)
    character_profiles: Mapped[list] = mapped_column(JSON)  # List of dicts
