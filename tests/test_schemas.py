from pydantic import ValidationError

from app.schemas.task import TaskRequestSchema, TaskStatus
from typing import Any
import pytest


class TestTaskStatus:
    def test_enum_values(self):
        assert TaskStatus.CREATED == "Created"
        assert TaskStatus.IN_PROGRESS == "In progress"
        assert TaskStatus.COMPLETED == "Completed"

    def test_enum_membership(self):
        assert "Created" in TaskStatus.__members__.values()
        assert "In progress" in TaskStatus.__members__.values()
        assert "Completed" in TaskStatus.__members__.values()

    def test_enum_iteration(self):
        expected_values = {"Created", "In progress", "Completed"}
        actual_values = {member.value for member in TaskStatus}
        assert actual_values == expected_values


class TestTaskBaseSchema:
    def test_valid_schema_creation(self, get_data_for_schema: dict[str, Any]):
        task = TaskRequestSchema(**get_data_for_schema)

        assert task.name == get_data_for_schema["name"], f"{task.name=}"
        assert task.description == get_data_for_schema["description"], (
            f"{task.description=}"
        )
        assert task.status == TaskStatus(get_data_for_schema["status"]), (
            f"{task.status=}"
        )
        assert isinstance(task.status, TaskStatus)

    @pytest.mark.parametrize("missing_field", ["name", "description", "status"])
    def test_missing_required_fields(
        self,
        get_data_for_schema: dict[str, Any],
        missing_field: str,
    ):
        invalid_data = get_data_for_schema.copy()
        del invalid_data[missing_field]

        with pytest.raises(ValidationError) as exc_info:
            TaskRequestSchema(**invalid_data)

        assert missing_field in str(exc_info.value)

    @pytest.mark.parametrize(
        "name",
        [
            "",  # empty
            "   ",  # too short min_length = 5
            "a" * 266,  # too_long max_length = 255
        ],
    )
    def test_invalid_name_values(self, get_data_for_schema: dict[str, Any], name: str):
        invalid_data = get_data_for_schema.copy()
        invalid_data["name"] = name

        with pytest.raises(ValidationError) as exception_info:
            TaskRequestSchema(**invalid_data)

        assert "name" in str(exception_info.value)

    @pytest.mark.parametrize(
        "description",
        [
            "",
            "   ",
        ],
    )
    def test_invalid_description_values(
        self,
        get_data_for_schema: dict[str, Any],
        description: str,
    ):
        invalid_data = get_data_for_schema.copy()
        invalid_data["description"] = description

        with pytest.raises(ValidationError) as exception_info:
            TaskRequestSchema(**invalid_data)

        assert "description" in str(exception_info.value)

    @pytest.mark.parametrize(
        "invalid_status",
        [
            "invalid_status",
            "pending",
            "done",
            "",
            None,
            123,
        ],
    )
    def test_invalid_status_values(
        self,
        get_data_for_schema: dict[str, Any],
        invalid_status: Any,
    ):
        invalid_data = get_data_for_schema.copy()
        invalid_data["status"] = invalid_status

        with pytest.raises(ValidationError) as exception_info:
            TaskRequestSchema(**invalid_data)

        assert "status" in str(exception_info.value)

    @pytest.mark.parametrize("valid_status", ["Created", "In progress", "Completed"])
    def test_valid_status_values(
        self,
        get_data_for_schema: dict[str, Any],
        valid_status: str,
    ):
        valid_data = get_data_for_schema.copy()
        valid_data["status"] = valid_status

        task = TaskRequestSchema(**valid_data)
        assert task.status == TaskStatus(valid_status), f"{task.status=}"

    def test_whitespace_stripping(self):
        data = {
            "name": "  Test Task  ",
            "description": "  Test Description  ",
            "status": "Created",
        }

        task = TaskRequestSchema(**data)
        assert task.name == "Test Task", f"{task.name=}"
        assert task.description == "Test Description", f"{task.description=}"

    def test_schema_json_serialization(self, get_data_for_schema: dict[str, Any]):
        task = TaskRequestSchema(**get_data_for_schema)
        json_data = task.model_dump_json()

        assert isinstance(json_data, str)
        assert get_data_for_schema["name"] in json_data, (
            f"{get_data_for_schema['name']} -> {json_data=}"
        )
        assert get_data_for_schema["description"] in json_data, (
            f"{get_data_for_schema['description']} -> {json_data=}"
        )

    def test_schema_dict_conversion(self, get_data_for_schema: dict[str, Any]):
        task = TaskRequestSchema(**get_data_for_schema)
        dict_data = task.model_dump()

        assert isinstance(dict_data, dict)
        assert dict_data["name"] == get_data_for_schema["name"], (
            f"{dict_data["name"]=} == {get_data_for_schema["name"]=}"
        )
        assert dict_data["description"] == get_data_for_schema["description"], (
            f"{dict_data["description"]=} == {get_data_for_schema['description']}"
        )
        assert dict_data["status"] == get_data_for_schema["status"], (
            f"{dict_data['status']} == {get_data_for_schema["status"]=}"
        )

    def test_field_descriptions(self):
        schema = TaskRequestSchema.model_json_schema()

        assert schema["properties"]["name"]["description"] == "Task name"
        assert schema["properties"]["description"]["description"] == "Task description"
        assert schema["properties"]["status"]["description"] == "Task status"

    @pytest.mark.parametrize(
        "field_name,min_length",
        [
            ("name", 1),
            ("description", 1),
        ],
    )
    def test_min_length_validation(
        self,
        get_data_for_schema: dict[str, Any],
        field_name: str,
        min_length: int,
    ):
        valid_data = get_data_for_schema.copy()

        invalid_data = valid_data.copy()
        invalid_data[field_name] = "a" * (min_length - 1)

        with pytest.raises(ValidationError) as exc_info:
            TaskRequestSchema(**invalid_data)

        assert field_name in str(exc_info.value)
        assert "at least" in str(exc_info.value).lower()
