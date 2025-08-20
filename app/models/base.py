from sqlalchemy.orm import mapped_column, Mapped
from uuid import UUID, uuid4
from sqlalchemy import DateTime
from app.config.database import database
from datetime import datetime
from sqlalchemy.sql import func


class BaseModel(database.Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        index=True,
        unique=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        onupdate=func.now(),
    )
