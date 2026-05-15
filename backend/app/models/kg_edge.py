import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class KGEdge(Base):
    __tablename__ = "kg_edges"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id: Mapped[str] = mapped_column(String(36), ForeignKey("kg_nodes.id"))
    target_id: Mapped[str] = mapped_column(String(36), ForeignKey("kg_nodes.id"))
    relation: Mapped[str] = mapped_column(String(100))
