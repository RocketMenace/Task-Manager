from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Type, Protocol
from app.models.base import BaseModel
from pydantic import BaseModel as Schema
from sqlalchemy import insert


ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepositoryProtocol(Protocol):
    async def create(self, schema: Schema) -> Type[ModelType]: ...


class BaseRepository(BaseRepositoryProtocol):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def create(self, schema: Schema) -> Type[ModelType]:
        instance = self.model(**schema.model_dump())
        try:
            async with self.session:
                query = insert(self.model).values(instance)
                result = await self.session.execute(query)
                return result.scalar_one()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Duplicate entry.",
            )

    # async def get(self, ) -> Type[ModelType]: