from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Summary(Base):
    __tablename__ = "summaries"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"))
    last_message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"))
    content: Mapped[str] = mapped_column(Text)
    
    # Relationships
    branch = relationship("Branch")
