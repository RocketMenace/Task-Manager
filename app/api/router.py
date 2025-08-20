from fastapi import APIRouter, status
from app.schemas.task import TaskResponseSchema, TaskRequestSchema
from dishka.integrations.fastapi import inject, FromDishka
from app.services.task import TaskService  # noqa
from app.schemas.base import ApiResponse
from app.schemas.pagination import ListPaginationResponse, PaginationResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Task creation.",
    response_model=ApiResponse[TaskResponseSchema],
)
@inject
async def create(data: TaskRequestSchema, service: FromDishka["TaskService"]):
    response = await service.create_task(schema=data)
    return ApiResponse(data=response)


@router.get(
    path="/{task_uuid}",
    status_code=status.HTTP_200_OK,
    summary="Retrieve task.",
    response_model=ApiResponse[TaskResponseSchema],
)
@inject
async def get(task_uuid: str, service: FromDishka["TaskService"]):
    response = await service.get_task_by_id(task_uuid=task_uuid)
    return ApiResponse(data=response)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    summary="Retrieve list of tasks",
    response_model=ApiResponse[ListPaginationResponse[TaskResponseSchema]],
)
@inject
async def get_list(
    offset: int,
    limit: int,
    service: FromDishka["TaskService"],
):
    response = await service.get_task_list(offset=offset, limit=limit)
    return ApiResponse(
        data=ListPaginationResponse(
            items=response,
            pagination=PaginationResponse(offset=offset, limit=limit),
        ),
    )
