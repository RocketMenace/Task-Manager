from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import ValidationError

from app.schemas.task import (
    TaskRequestSchema,
    TaskStatus,
    TaskResponseSchema,
    TaskBaseSchema,
)
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


class TestTaskResponseSchemaStructure:
    def test_inherits_from_task_base_schema(self):
        assert issubclass(TaskResponseSchema, TaskBaseSchema)

    def test_has_additional_fields(self):
        schema = TaskResponseSchema.model_json_schema()
        assert "id" in schema.get("properties"), f"id -> {schema.get("properties")=}"
        assert "created_at" in schema.get("properties"), (
            f"created_at -> {schema.get("properties")=}"
        )
        assert "name" in schema.get("properties"), (
            f"name -> {schema.get("properties")=}"
        )
        assert "description" in schema.get("properties"), (
            f"description -> {schema.get("properties")=}"
        )
        assert "status" in schema.get("properties"), (
            f"status -> {schema.get("properties")=}"
        )

    def test_field_descriptions(self):
        schema = TaskResponseSchema.model_json_schema()

        assert schema.get("properties").get("id").get("description") == "Task id."
        assert (
            schema.get("properties").get("created_at").get("description")
            == "Task creation date."
        )
        assert schema.get("properties").get("name").get("description") == "Task name"
        assert (
            schema.get("properties").get("description").get("description")
            == "Task description"
        )
        assert (
            schema.get("properties").get("status").get("description") == "Task status"
        )


class TestTaskResponseSchemaValidation:
    def test_valid_schema_creation(self, task_response_data: dict[str, Any]):
        task = TaskResponseSchema(**task_response_data)

        assert task.id == task_response_data.get("id"), (
            f"{task.id=} == {task_response_data.get("id")=}"
        )
        assert task.name == task_response_data.get("name"), (
            f"{task.name=} == {task_response_data=}"
        )
        assert task.description == task_response_data.get("description"), (
            f"{task.description=} == {task_response_data.get('description')}"
        )
        assert task.status == TaskStatus(task_response_data.get("status")), (
            f"{task.status=} == TaskStatus{task_response_data.get('status')}"
        )
        assert task.created_at == task_response_data.get("created_at"), (
            f"{task.created_at=} == {task_response_data.get("created_at")=}"
        )
        assert isinstance(task.id, UUID)
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.status, TaskStatus)

    @pytest.mark.parametrize(
        "missing_field",
        ["id", "created_at", "name", "description", "status"],
    )
    def test_missing_required_fields(
        self,
        task_response_data: dict[str, Any],
        missing_field: str,
    ):
        invalid_data = task_response_data.copy()
        del invalid_data[missing_field]

        with pytest.raises(ValidationError) as exception_info:
            TaskResponseSchema(**invalid_data)

        assert missing_field in str(exception_info.value), (
            f"{missing_field=} -> {str(exception_info.value)=}"
        )

    def test_invalid_uuid_format(self, task_response_data: dict[str, Any]):
        invalid_data = task_response_data.copy()
        invalid_data["id"] = "not-a-valid-uuid"

        with pytest.raises(ValidationError) as exception_info:
            TaskResponseSchema(**invalid_data)

        assert "id" in str(exception_info.value), f"id -> {str(exception_info.value)=}"
        assert "UUID" in str(exception_info.value), (
            f"UUID -> {str(exception_info.value)=}"
        )

    def test_invalid_datetime_format(self, task_response_data: dict[str, Any]):
        invalid_data = task_response_data.copy()
        invalid_data["created_at"] = "not-a-valid-datetime"

        with pytest.raises(ValidationError) as exception_info:
            TaskResponseSchema(**invalid_data)

        assert "created_at" in str(exception_info.value), (
            f"created_at -> {str(exception_info.value)=}"
        )
        assert "datetime" in str(exception_info.value), (
            f"datetime -> {str(exception_info.value)=}"
        )

    def test_null_values_rejected(self, task_response_data: dict[str, Any]):
        for field in ["id", "created_at", "name", "description", "status"]:
            invalid_data = task_response_data.copy()
            invalid_data[field] = None

            with pytest.raises(ValidationError) as exception_info:
                TaskResponseSchema(**invalid_data)

            assert field in str(exception_info.value), (
                f"{field=} -> {str(exception_info.value)=}"
            )


class TestTaskResponseSchemaSerialization:
    def test_json_serialization(self, task_response_instance: TaskResponseSchema):
        json_data = task_response_instance.model_dump_json()

        assert isinstance(json_data, str)
        assert str(task_response_instance.id) in json_data, (
            f"{str(task_response_instance.id)=} -> {json_data=}"
        )
        assert task_response_instance.name in json_data, (
            f"{task_response_instance.name=} -> {json_data=}"
        )

    def test_dict_serialization(self, task_response_instance: TaskResponseSchema):
        dict_data = task_response_instance.model_dump()

        assert isinstance(dict_data, dict)
        assert dict_data.get("id") == task_response_instance.id, (
            f"{dict_data.get('id')} == {task_response_instance.id=}"
        )
        assert dict_data.get("name") == task_response_instance.name, (
            f"{dict_data.get("name")=} == {task_response_instance.name=}"
        )
        assert dict_data.get("created_at") == task_response_instance.created_at, (
            f"{dict_data.get("created_at")=} == {task_response_instance.created_at=}"
        )

    def test_json_deserialization(self, task_response_instance: TaskResponseSchema):
        json_data = task_response_instance.model_dump_json()
        deserialized = TaskResponseSchema.model_validate_json(json_data)

        assert deserialized.id == task_response_instance.id, (
            f"{deserialized.id=} == {task_response_instance.id=}"
        )
        assert deserialized.name == task_response_instance.name, (
            f"{deserialized.name=} == {task_response_instance.name=}"
        )
        assert deserialized.created_at == task_response_instance.created_at, (
            f"{deserialized.created_at=} == {task_response_instance.created_at=}"
        )


class TestTaskResponseSchemaFromAttributes:
    def test_model_config_from_attributes(self):
        config = TaskResponseSchema.model_config
        assert "from_attributes" in config, f"from_attributes -> {config=}"
        assert config.get("from_attributes") is True

    def test_can_create_from_orm_model(self):
        class MockORMModel:
            def __init__(self):
                self.id = uuid4()
                self.name = "Test Task"
                self.description = "Test Description"
                self.status = "Created"
                self.created_at = datetime.now(timezone.utc)

        orm_model = MockORMModel()

        schema_instance = TaskResponseSchema.model_validate(orm_model)

        assert schema_instance.id == orm_model.id, (
            f"{schema_instance.id=} == {orm_model.id=}"
        )
        assert schema_instance.name == orm_model.name, (
            f"{schema_instance.name=} == {orm_model.id=}"
        )
        assert schema_instance.description == orm_model.description, (
            f"{schema_instance.description=} == {orm_model.description}"
        )


class TestTaskResponseSchemaEdgeCases:
    @pytest.mark.parametrize("uuid_version", [1, 4, 5])
    def test_different_uuid_versions(
        self,
        task_response_data: dict[str, Any],
        uuid_version: int,
    ):
        test_data = task_response_data.copy()

        if uuid_version == 1:
            test_data["id"] = uuid4()
        elif uuid_version == 5:
            test_data["id"] = UUID("{12345678-1234-5678-1234-567812345678}")

        task = TaskResponseSchema(**test_data)
        assert isinstance(task.id, UUID)

    def test_timezone_aware_datetime(self, task_response_data: dict[str, Any]):
        test_data = task_response_data.copy()
        test_data["created_at"] = datetime.now(timezone.utc)

        task = TaskResponseSchema(**test_data)
        assert task.created_at.tzinfo is not None

    def test_very_old_datetime(self, task_response_data: dict[str, Any]):
        test_data = task_response_data.copy()
        test_data["created_at"] = datetime(1970, 1, 1)

        task = TaskResponseSchema(**test_data)
        assert task.created_at.year == 1970

    def test_future_datetime(self, task_response_data: dict[str, Any]):
        test_data = task_response_data.copy()
        test_data["created_at"] = datetime(2030, 1, 1)

        task = TaskResponseSchema(**test_data)
        assert task.created_at.year == 2030
