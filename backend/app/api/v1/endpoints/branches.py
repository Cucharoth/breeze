from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.message import MessageCreate, MessageRead
from app.schemas.checkpoint import CheckpointCreate, CheckpointRead
from app.schemas.kg import KGGraphRead
from app.services.story_service import story_service
from app.services.memory_pipeline import extract_knowledge
from app.repositories.kg_repository import kg_repository
from app.api.dependencies import get_llm_adapter

router = APIRouter()

@router.post("/{branch_id}/messages/", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
async def add_message(
    branch_id: int,
    message_in: MessageCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    llm_adapter = Depends(get_llm_adapter)
):
    message = await story_service.add_message(db, branch_id, message_in.role, message_in.content)
    
    # Trigger background knowledge extraction
    background_tasks.add_task(extract_knowledge, branch_id, message_in.content, llm_adapter)
    
    return message

@router.post("/{branch_id}/checkpoints/", response_model=CheckpointRead, status_code=status.HTTP_201_CREATED)
async def create_checkpoint(
    branch_id: int,
    checkpoint_in: CheckpointCreate,
    db: AsyncSession = Depends(get_db)
):
    return await story_service.create_checkpoint(db, branch_id, checkpoint_in.message_id)

@router.get("/{branch_id}/history/", response_model=List[MessageRead])
async def get_history(
    branch_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await story_service.get_history(db, branch_id)

@router.post("/{branch_id}/summarize/")
async def summarize(
    branch_id: int,
    db: AsyncSession = Depends(get_db),
    llm_adapter = Depends(get_llm_adapter)
):
    summary = await story_service.generate_summary(db, branch_id, llm_adapter)
    return {"summary": summary}

@router.get("/{branch_id}/kg/", response_model=KGGraphRead)
async def get_kg(
    branch_id: int,
    db: AsyncSession = Depends(get_db)
):
    nodes = await kg_repository.get_nodes(db, branch_id)
    edges = await kg_repository.get_edges(db, branch_id)
    return {"nodes": nodes, "edges": edges}
