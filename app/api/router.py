from fastapi import APIRouter, status
from app.schemas.task import TaskResponseSchema, TaskRequestSchema
from dishka.integrations.fastapi import inject, FromDishka
from app.services.task import TaskService # noqa
from app.schemas.base import ApiResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    summary="Task creation",
    response_model=ApiResponse[TaskResponseSchema],
)
@inject
async def create(data: TaskRequestSchema, service: FromDishka["TaskService"]):
    response = await service.create_task(schema=data)
    return ApiResponse(data=response)
