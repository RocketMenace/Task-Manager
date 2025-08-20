from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Type, Protocol, Sequence


from app.models.base import BaseModel
from pydantic import BaseModel as Schema
from sqlalchemy import select, delete


ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepositoryProtocol(Protocol):
    async def create(self, schema: Schema) -> Type[ModelType]: ...
    async def get_by_uuid(self, uuid: str) -> Type[ModelType]: ...
    async def get_list(self, offset: int, limit: int) -> Sequence[Type[ModelType]]: ...
    async def update(self, uuid: str) -> Type[ModelType]: ...
    async def delete(self, uuid: str) -> None: ...


class BaseRepository(BaseRepositoryProtocol):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def create(self, schema: Schema) -> Type[ModelType]:
        instance = self.model(**schema.model_dump())
        try:
            async with self.session as session:
                session.add(instance=instance)
                await session.commit()
                await session.refresh(instance=instance)
                return instance
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Duplicate entry.",
            )

    async def get_by_uuid(self, uuid: str) -> Type[ModelType] | None:
        async with self.session as session:
            try:
                query = select(self.model).where(self.model.id == uuid)
                result = await session.execute(query)
                return result.one_or_none()
            except SQLAlchemyError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid UUID.",
                )

    async def get_list(self, offset: int, limit: int) -> Sequence[Type[ModelType]]:
        async with self.session as session:
            query = select(self.model).offset(offset=offset).limit(limit=limit)
            result = await session.scalars(query)
            return result.all()

    async def update(self, uuid: str) -> Type[ModelType] | None:
        async with self.session:
            query = select(self.model).where(self.model.id == uuid)
            result = await self.session.execute(query)
            if not result:
                return None

    async def delete(self, uuid: str) -> None:
        async with self.session:
            query = delete(self.model).where(self.model.id == uuid)
            await self.session.execute(query)
