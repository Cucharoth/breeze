from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.scenario_repository import scenario_repository
from app.schemas.scenario import ScenarioCreate
from app.models.scenario import Scenario
from app.services.llm_service import LLMService
from app.core.logger import logger

class ScenarioService:
    async def create_scenario(
        self, 
        db: AsyncSession, 
        scenario_in: ScenarioCreate,
        llm_service: LLMService
    ) -> Scenario:
        """
        Create a new scenario by generating lore and content using the LLM service.
        """
        logger.debug(f"Service: Starting generation for premise '{scenario_in.premise[:30]}'")
        
        # Generate world lore, first scene, and characters using the orchestrated service
        scenario_data = await llm_service.generate_scenario(scenario_in.premise)
        
        logger.debug("Service: LLM generation complete, persisting to database")
        
        # Merge with input data (the premise)
        obj_in_data = {
            "premise": scenario_in.premise,
            **scenario_data
        }
        
        scenario = await scenario_repository.create(db, obj_in_data=obj_in_data)
        logger.debug(f"Service: Scenario persisted with ID {scenario.id}")
        return scenario

scenario_service = ScenarioService()
