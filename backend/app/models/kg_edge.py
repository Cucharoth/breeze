from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class KGEdge(Base):
    __tablename__ = "kg_edges"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"))
    source_node_id: Mapped[int] = mapped_column(ForeignKey("kg_nodes.id"))
    target_node_id: Mapped[int] = mapped_column(ForeignKey("kg_nodes.id"))
    relationship: Mapped[str] = mapped_column(String(100))
