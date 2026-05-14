from app.repositories.base_repository import BaseRepository
from app.models.summary import Summary
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

class SummaryRepository(BaseRepository[Summary]):
    async def get_latest_for_branch(self, db: AsyncSession, branch_id: int) -> Optional[Summary]:
        result = await db.execute(
            select(Summary)
            .where(Summary.branch_id == branch_id)
            .order_by(Summary.id.desc())
        )
        return result.scalars().first()

summary_repository = SummaryRepository(Summary)
