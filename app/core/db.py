import asyncio
import hashlib

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings
from app.models import Users

engine = create_async_engine(
    url=settings.POSTGRES, echo=False, pool_pre_ping=True
)



async_db_session = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def db_session() -> AsyncSession:
    async with async_db_session() as session:
        yield session



# async def test():
#
#     async with async_db_session() as dbsession:
#
#         stmt = select(Users).where(
#             Users.login == "2"
#         )
#         result = await dbsession.execute(statement=stmt)
#         print(result.one_or_none())
#
#
#
#
# asyncio.run(test())





