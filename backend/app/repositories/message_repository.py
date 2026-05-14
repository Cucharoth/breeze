from app.repositories.base_repository import BaseRepository
from app.models.message import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

class MessageRepository(BaseRepository[Message]):
    async def get_branch_history(self, db: AsyncSession, branch_id: int) -> List[Message]:
        # To handle branching properly, we need to walk up the tree
        # For the first pass, we'll implement a simple recursive fetch or a list of IDs
        # Let's start with a simple version that only gets current branch messages
        # We will add the "ancestry" logic in the service or improve this repository method
        result = await db.execute(
            select(Message)
            .where(Message.branch_id == branch_id)
            .order_by(Message.created_at.asc())
        )
        return list(result.scalars().all())

message_repository = MessageRepository(Message)
