from typing import AsyncIterator, Generator
import httpx
import pytest_asyncio
from fastapi.testclient import TestClient
from app.main import app
import pytest
from faker import Faker
from typing import Any
from uuid import uuid4
from datetime import datetime, timezone
from app.schemas.task import TaskResponseSchema

fake = Faker()


@pytest.fixture
def get_client() -> Generator:
    yield TestClient(app=app)


@pytest_asyncio.fixture
async def get_async_client(get_client) -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url=get_client.base_url,
    ) as client:
        yield client


@pytest.fixture
def get_data_for_schema() -> dict:
    return {
        "name": fake.sentence(nb_words=3),
        "description": fake.paragraph(),
        "status": "Created",
    }


@pytest.fixture
def task_response_data() -> dict[str, Any]:
    return {
        "id": uuid4(),
        "name": fake.sentence(nb_words=3),
        "description": fake.paragraph(),
        "status": "Created",
        "created_at": datetime.now(timezone.utc),
    }


@pytest.fixture
def task_response_instance(task_response_data: dict[str, Any]) -> TaskResponseSchema:
    return TaskResponseSchema(**task_response_data)
