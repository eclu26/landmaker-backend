from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.settings import settings


DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.db_user}:{settings.db_password}@"
    f"{settings.db_host}:{settings.db_port}/"
    f"{settings.db_name}"
)


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False
)


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception:
                await session.rollback()
                raise

    return wrapper

async def get_session():
    async with async_session_maker() as session:
        yield session