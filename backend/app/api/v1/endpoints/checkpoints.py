from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.branch import BranchRead, BranchCreate
from app.services.story_service import story_service

router = APIRouter()

@router.post("/{checkpoint_id}/branches/", response_model=BranchRead, status_code=status.HTTP_201_CREATED)
async def spawn_branch(
    checkpoint_id: int,
    branch_in: BranchCreate,
    db: AsyncSession = Depends(get_db)
):
    return await story_service.spawn_branch(db, checkpoint_id, branch_in.name)
