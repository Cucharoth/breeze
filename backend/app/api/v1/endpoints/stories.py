from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.story import StoryRead, StoryTreeRead
from app.services.story_service import story_service

router = APIRouter()

@router.post("/", response_model=StoryRead, status_code=status.HTTP_201_CREATED)
async def create_story(
    scenario_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await story_service.create_story(db, scenario_id)

@router.get("/{story_id}/tree", response_model=StoryTreeRead)
async def get_story_tree(
    story_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await story_service.get_story_tree(db, story_id)
