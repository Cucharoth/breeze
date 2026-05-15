from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.models.checkpoint import Checkpoint

class CheckpointRepository(BaseRepository[Checkpoint]):
    async def get_multi_by_branches(self, db: AsyncSession, branch_ids: list[str]):
        result = await db.execute(select(Checkpoint).where(Checkpoint.branch_id.in_(branch_ids)))
        return list(result.scalars().all())

checkpoint_repository = CheckpointRepository(Checkpoint)
