from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from uuid import UUID
from datetime import datetime
from typing import Any


class TaskStatus(str, Enum):
    CREATED = "Created"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"


class TaskBaseSchema(BaseModel):
    name: str = Field(..., description="Task name")
    description: str = Field(..., description="Task description")
    status: TaskStatus = Field(..., description="Task status")


class TaskRequestSchema(TaskBaseSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "name": "Parcel delivery.",
            "description": "Deliver parcel to specified address.",
            "status": "Created",
        },
    )


class TaskUpdateSchema(TaskBaseSchema):
    name: str | None = Field(..., description="Task name")
    description: str | None = Field(..., description="Task description")
    status: TaskStatus | None = Field(..., description="Task status")


class TaskResponseSchema(TaskBaseSchema):
    id: UUID = Field(..., description="Task id.")
    created_at: datetime = Field(..., description="Task creation date.")
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "name": "Parcel delivery.",
            "description": "Deliver parcel to specified address.",
            "status": "Created",
        },
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        return TaskResponseSchema(**data)
