from typing import AsyncIterator, Generator
import httpx
import pytest_asyncio
from fastapi.testclient import TestClient
from app.main import app
import pytest
from faker import Faker

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
