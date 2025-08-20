from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from .base import BaseRepository


class TaskRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        super().__init__(session=session, model=Task)
