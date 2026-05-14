from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.scenario import ScenarioCreate, ScenarioRead
from app.services.scenario_service import scenario_service

router = APIRouter()

@router.post("/", response_model=ScenarioRead, status_code=status.HTTP_201_CREATED)
async def create_scenario(
    scenario_in: ScenarioCreate,
    db: AsyncSession = Depends(get_db)
):
    return await scenario_service.create_scenario(db, scenario_in)
