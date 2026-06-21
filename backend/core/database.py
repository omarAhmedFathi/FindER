from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from core.config import settings

# Optimized pool configuration: min=5, max=20, max_overflow=10, 30s query timeout
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=False, 
    pool_size=5, 
    max_overflow=15,
    pool_timeout=30,
    connect_args={"command_timeout": 30}
)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
