from app.repositories.base_repository import BaseRepository
from app.models.story import Story

class StoryRepository(BaseRepository[Story]):
    pass

story_repository = StoryRepository(Story)
