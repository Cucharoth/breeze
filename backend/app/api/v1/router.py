from fastapi import APIRouter
from app.api.v1.endpoints import scenarios, stories, branches, checkpoints

api_router = APIRouter()
api_router.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])
api_router.include_router(stories.router, prefix="/stories", tags=["stories"])
api_router.include_router(branches.router, prefix="/branches", tags=["branches"])
api_router.include_router(checkpoints.router, prefix="/checkpoints", tags=["checkpoints"])
