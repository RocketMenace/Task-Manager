from asyncio import AbstractEventLoop
from typing import AsyncIterator, Generator, AsyncGenerator, Iterator
import httpx
import pytest_asyncio
from dishka import make_async_container
from fastapi.testclient import TestClient
import asyncio


from app.main import create_app
import pytest
from faker import Faker
from typing import Any
from uuid import uuid4
from datetime import datetime, timezone
from app.schemas.task import TaskResponseSchema
from app.providers import (
    MockSessionProvider,
    TaskRepositoryProvider,
    TaskServiceProvider,
)
from dishka.integrations.fastapi import setup_dishka

fake = Faker()

@pytest.fixture(scope='session')
def event_loop() -> Iterator[AbstractEventLoop]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def get_async_client(container) -> AsyncIterator[httpx.AsyncClient]:
    app = create_app()
    setup_dishka(container=container, app=app)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://localhost:8000",
    ) as client:
        yield client


@pytest.fixture
def get_data_for_schema() -> dict:
    return {
        "name": fake.sentence(nb_words=5),
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


@pytest_asyncio.fixture
async def container():
    container = make_async_container(
        MockSessionProvider(), TaskRepositoryProvider(), TaskServiceProvider()
    )
    yield container
    await container.close()
