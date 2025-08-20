from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Type, Protocol, Sequence


from app.models.base import BaseModel
from pydantic import BaseModel as Schema
from sqlalchemy import select, update, delete, insert

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepositoryProtocol(Protocol):
    async def create(self, schema: Schema) -> Type[ModelType]: ...
    async def get_by_uuid(self, uuid: str) -> Type[ModelType]: ...
    async def get_list(self, offset: int, limit: int) -> Sequence[Type[ModelType]]: ...
    async def update(self, uuid: str, schema: Schema) -> Type[ModelType]: ...
    async def delete(self, uuid: str) -> None: ...


class BaseRepository(BaseRepositoryProtocol):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def create(self, schema: Schema) -> Type[ModelType]:
        try:
            async with self.session as session:
                query = (
                    insert(self.model).values(schema.model_dump()).returning(self.model)
                )
                result = await session.execute(query)
                return result.scalar_one()
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
                return result.scalar_one()
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

    async def update(self, uuid: str, schema: Schema) -> Type[ModelType] | None:
        try:
            async with self.session as session:
                query = (
                    update(self.model)
                    .where(self.model.id == uuid)
                    .values(**schema.model_dump())
                ).returning(self.model)
                result = await session.execute(query)
                return result.scalar_one()

        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid UUID.",
            )

    async def delete(self, uuid: str) -> None:
        try:
            async with self.session as session:
                query = delete(self.model).where(self.model.id == uuid)
                await session.execute(query)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid UUID.",
            )
