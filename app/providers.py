from dishka import Scope, provide, Provider
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task import TaskRepository
from app.services.task import TaskService

from app.config.database import database


class SessionProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_session(self) -> AsyncSession:
        return database.get_session()


class TaskRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_repository(self, session: AsyncSession) -> TaskRepository:
        return TaskRepository(session=session)


class TaskServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_service(self, repository: TaskRepository) -> TaskService:
        return TaskService(repository=repository)
