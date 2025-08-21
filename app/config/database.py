from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base
from .settings import settings


class Database:
    def __init__(self, url: str):
        self._async_engine = create_async_engine(
            url=url,
            pool_pre_ping=True,
            echo=True,
        )
        self._async_session = async_sessionmaker(
            bind=self._async_engine,
            expire_on_commit=False,
            autocommit=False
        )
        self.Base = declarative_base()

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
        session: AsyncSession = self._async_session()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.commit()
            await session.close()

    @asynccontextmanager
    async def get_test_session(self) -> AsyncGenerator[AsyncSession, Any]:
        session: AsyncSession = self._async_session()
        try:
            async with session:
                await session.begin_nested()
                try:
                    yield session
                finally:
                    if session.in_transaction():
                        await session.rollback()
        finally:
            await session.close()




database = Database(url=settings.db_url)
