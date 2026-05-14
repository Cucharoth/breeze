from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import get_settings
from app.core.logger import setup_logging, logger
from app.core.database import engine, Base
import app.models

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    logger.info(f"Starting {settings.PROJECT_NAME} backend...")
    
    # Create tables
    async with engine.begin() as conn:
        # In a real app, use Migrations (Alembic)
        # But for this minimalist setup, we'll create them on startup
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.PROJECT_NAME} backend...")
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# Include routers
from app.api.v1.router import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
