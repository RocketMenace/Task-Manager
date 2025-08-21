import asyncio

import pytest
from httpx import AsyncClient
from fastapi import status
import uuid
from datetime import datetime


class TestTaskCreationIntegration:
    """Tests with mocked database."""

    @pytest.mark.asyncio
    async def test_create_task_success(
        self, get_async_client: AsyncClient, get_data_for_schema: dict
    ):
        response = await get_async_client.post("/api/tasks/", json=get_data_for_schema)

        assert response.status_code == status.HTTP_201_CREATED, (
            f"{response.status_code=} == {status.HTTP_201_CREATED=}"
        )
        response_data = response.json()

        assert "data" in response_data
        assert "meta" in response_data
        assert "errors" in response_data
        assert response_data.get("errors") == []

        task_data = response_data["data"]
        assert task_data.get("name") == get_data_for_schema.get("name")
        assert task_data.get("description") == get_data_for_schema.get("description")
        assert task_data.get("status") == get_data_for_schema.get("status")
        assert "id" in task_data
        assert "created_at" in task_data
        assert uuid.UUID(task_data.get("id"))
        assert datetime.fromisoformat(
            task_data.get("created_at").replace("Z", "+00:00")
        )

    @pytest.mark.asyncio
    async def test_create_task_with_missing_required_fields(
        self, get_async_client: AsyncClient
    ):
        # Act
        response = await get_async_client.post(
            "/api/tasks/", json={"name": "Test Task"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert "detail" in response_data

    @pytest.mark.asyncio
    async def test_create_task_with_invalid_status(self, get_async_client: AsyncClient):
        response = await get_async_client.post(
            "/api/tasks/",
            json={
                "name": "Test Task",
                "description": "Test description",
                "status": "InvalidStatus",
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert "detail" in response_data

    @pytest.mark.asyncio
    async def test_create_task_empty_name(self, get_async_client: AsyncClient):
        response = await get_async_client.post(
            "/tasks/",
            json={"name": "", "description": "Test description", "status": "Created"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert "detail" in response_data


class TestTaskCreationEdgeCases:

    @pytest.mark.asyncio
    async def test_create_task_with_long_values(self, get_async_client: AsyncClient):
        long_name = "A" * 300

        response = await get_async_client.post(
            "/api/tasks/",
            json={
                "name": long_name,
                "description": "Some description",
                "status": "Created",
            },
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_create_task_with_special_characters(
        self, get_async_client: AsyncClient
    ):
        response = await get_async_client.post(
            "/api/tasks/",
            json={
                "name": "Task with spéciål chàräctérs!@#$%^&*()",
                "description": "Description with unicode: ñáéíóú",
                "status": "Created",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.asyncio
    async def test_create_task_with_whitespace(self, get_async_client: AsyncClient):
        response = await get_async_client.post(
            "/api/tasks/",
            json={
                "name": "   Test Task   ",
                "description": "   Test description   ",
                "status": "Created",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data.get("data").get("name") == "Test Task"

    @pytest.mark.asyncio
    async def test_create_task_malformed_json(self, get_async_client: AsyncClient):
        response = await get_async_client.post(
            "/api/tasks/",
            content="{invalid json",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_create_task_wrong_content_type(self, get_async_client: AsyncClient):
        response = await get_async_client.post(
            "/api/tasks/",
            data={"name": "Test Task"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
class TestTaskCreationPerformance:

    async def test_create_multiple_tasks_sequential(self, get_async_client: AsyncClient):
        tasks_to_create = 10

        for i in range(tasks_to_create):
            response = await get_async_client.post(
                "/api/tasks/",
                json={
                    "name": f"Task {i}",
                    "description": f"Description for task {i}",
                    "status": "Created"
                }
            )
            assert response.status_code == status.HTTP_201_CREATED

    async def test_create_multiple_tasks_concurrent(self, get_async_client: AsyncClient, get_data_for_schema):
        tasks_to_create = 10

        async def create_task(i):
            response = await get_async_client.post(
                "/api/tasks/",
                json=get_data_for_schema
            )
            assert response.status_code == status.HTTP_201_CREATED
            return response

        results = await asyncio.gather(
            *(create_task(i) for i in range(tasks_to_create))
        )

        assert len(results) == tasks_to_create
        assert all(result.status_code == status.HTTP_201_CREATED for result in results)
