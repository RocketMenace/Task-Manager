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
            isolation_level="READ COMMITTED",
        )
        self._async_session = async_sessionmaker(
            bind=self._async_engine,
            expire_on_commit=False,
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
        async with session:
            async with self._async_engine.begin() as conn:
                await conn.run_sync(database.Base.metadata.create_all)
            transaction = await session.begin()
            try:
                yield session
            finally:
                if transaction.is_active:
                    await transaction.rollback()
                await session.close()


database = Database(url=settings.db_url)
