from app.repositories.base_repository import BaseRepository
from app.models.checkpoint import Checkpoint

class CheckpointRepository(BaseRepository[Checkpoint]):
    pass

checkpoint_repository = CheckpointRepository(Checkpoint)
