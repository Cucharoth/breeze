from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.branch import Branch

class BranchRepository(BaseRepository[Branch]):
    async def get_multi_by_story(self, db: AsyncSession, story_id: str):
        result = await db.execute(select(Branch).where(Branch.story_id == story_id))
        return list(result.scalars().all())

branch_repository = BranchRepository(Branch)
