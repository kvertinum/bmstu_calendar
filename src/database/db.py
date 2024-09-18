from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import DB_URL


engine = create_async_engine(DB_URL)
session_pool: sessionmaker[AsyncSession] = sessionmaker(
    engine, class_=AsyncSession
)


class Base(AsyncAttrs, DeclarativeBase):
    pass
