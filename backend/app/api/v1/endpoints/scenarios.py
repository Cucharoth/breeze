from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.scenario import ScenarioCreate, ScenarioRead
from app.services.scenario_service import scenario_service

from app.api.dependencies import get_llm_service
from app.services.llm_service import LLMService

from app.core.logger import logger

router = APIRouter()

@router.post("/", response_model=ScenarioRead, status_code=status.HTTP_201_CREATED)
async def create_scenario(
    scenario_in: ScenarioCreate,
    db: AsyncSession = Depends(get_db),
    llm_service: LLMService = Depends(get_llm_service)
):
    logger.info(f"Igniting reality with premise: {scenario_in.premise[:50]}...")
    return await scenario_service.create_scenario(db, scenario_in, llm_service)

@router.get("/{scenario_id}", response_model=ScenarioRead)
async def get_scenario(
    scenario_id: str,
    db: AsyncSession = Depends(get_db)
):
    from app.repositories.scenario_repository import scenario_repository
    scenario = await scenario_repository.get(db, scenario_id)
    if not scenario:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario

@router.patch("/{scenario_id}", response_model=ScenarioRead)
async def update_scenario(
    scenario_id: str,
    scenario_update: dict, # Simplified for now
    db: AsyncSession = Depends(get_db)
):
    from app.repositories.scenario_repository import scenario_repository
    scenario = await scenario_repository.get(db, scenario_id)
    if not scenario:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    return await scenario_repository.update(db, db_obj=scenario, obj_in=scenario_update)
