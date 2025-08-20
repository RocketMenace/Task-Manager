import pytest
from fastapi import status
import httpx


@pytest.mark.asyncio
async def test_app_startup(get_async_client: httpx.AsyncClient):
    response = await get_async_client.get("/docs")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_redoc(get_async_client):
    response = await get_async_client.get("/redoc")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_openapi_json(get_async_client):
    response = await get_async_client.get("/openapi.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "Task Manager API"
