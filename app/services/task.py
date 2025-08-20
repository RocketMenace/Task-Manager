from app.repositories.base import BaseRepository
from app.schemas.task import TaskRequestSchema, TaskResponseSchema
from typing import Any


class TaskService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def create_task(self, schema: TaskRequestSchema):
        return await self.repository.create(schema=schema)
