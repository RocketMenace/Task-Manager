from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Enum as SQLEnum
from enum import Enum

from .base import BaseModel


class StatusType(str, Enum):
    CREATED = "Created"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"


class Task(BaseModel):
    __tablename__ = "tasks"

    name: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[StatusType] = mapped_column(
        SQLEnum(StatusType),
        default=StatusType.CREATED,
    )
