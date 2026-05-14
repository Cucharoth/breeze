from app.repositories.base_repository import BaseRepository
from app.models.branch import Branch

class BranchRepository(BaseRepository[Branch]):
    pass

branch_repository = BranchRepository(Branch)
