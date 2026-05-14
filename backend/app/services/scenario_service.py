from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.scenario_repository import scenario_repository
from app.schemas.scenario import ScenarioCreate
from app.models.scenario import Scenario

class ScenarioService:
    async def create_scenario(self, db: AsyncSession, scenario_in: ScenarioCreate) -> Scenario:
        # Mock generation logic
        # In the future, this will call an LLM Adapter
        scenario_data = {
            "premise": scenario_in.premise,
            "world_lore": f"World lore for: {scenario_in.premise}",
            "first_scene": "You wake up in a dimly lit room...",
            "character_profiles": [{"name": "Protagonist", "description": "The main character"}]
        }
        return await scenario_repository.create(db, obj_in_data=scenario_data)

scenario_service = ScenarioService()
