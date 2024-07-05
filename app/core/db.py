
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings

engine = create_async_engine(
    url=settings.POSTGRES, echo=False, pool_pre_ping=True
)

async_db_session = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def db_session() -> AsyncSession:
    async with async_db_session() as session:
        yield session





