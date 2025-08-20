from typing import Sequence

from app.repositories.base import BaseRepository
from app.schemas.task import TaskRequestSchema
from app.models.task import Task


class TaskService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def create_task(self, schema: TaskRequestSchema) -> Task:
        """
        :param schema:
                 - "name"
                 - "description"
                 - "status"
            :return: <class 'app.models.task.Task'>
        """
        return await self.repository.create(schema=schema)

    async def get_task_by_id(self, task_uuid: str) -> Task | None:
        return await self.repository.get_by_uuid(uuid=task_uuid)

    async def get_task_list(self, offset: int, limit: int) -> Sequence[Task]:
        return await self.repository.get_list(offset=offset, limit=limit)

    async def delete_task(self, task_uuid: str) -> None:
        return await self.repository.delete(uuid=task_uuid)
