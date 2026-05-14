from app.repositories.base_repository import BaseRepository
from app.models.scenario import Scenario

class ScenarioRepository(BaseRepository[Scenario]):
    pass

scenario_repository = ScenarioRepository(Scenario)
