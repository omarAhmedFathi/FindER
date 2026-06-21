import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.database import Base, get_db
from main import app
from utils.password import get_password_hash
from api.v1.auth.models import User, UserRole

# Test DB (In-memory SQLite for speed during async tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function")
async def async_db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    session = TestingSessionLocal()
    yield session
    await session.close()
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def async_client(async_db_session):
    async def override_get_db():
        yield async_db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def test_user(async_db_session):
    user = User(
        email="medic@finder.app",
        hashed_password=get_password_hash("securepass123"),
        full_name="Jane Doe",
        role=UserRole.FIELD_MEDIC
    )
    async_db_session.add(user)
    await async_db_session.commit()
    return user
