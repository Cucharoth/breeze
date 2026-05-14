import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app as fastapi_app
from app.core.database import get_db, Base
import app.models
from app.core.config import get_settings

TEST_DATABASE_URL = "sqlite+aiosqlite:///file:testdb?mode=memory&cache=shared&uri=true"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def db_session():
    # Setup
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Override global AsyncSessionLocal so background tasks use the test DB
    import app.core.database
    original_session_local = app.core.database.AsyncSessionLocal
    app.core.database.AsyncSessionLocal = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with app.core.database.AsyncSessionLocal() as session:
        yield session
        # Cleanup
        await session.close()
    
    app.core.database.AsyncSessionLocal = original_session_local
    await engine.dispose()

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    fastapi_app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), 
        base_url="http://test"
    ) as ac:
        yield ac
    
    fastapi_app.dependency_overrides.clear()
