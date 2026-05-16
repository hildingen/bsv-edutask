import uuid
from unittest.mock import patch
import pytest
from pymongo.errors import WriteError
from src.util.dao import DAO

USER_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["firstName", "lastName", "email"],
        "properties": {
            "firstName": {
                "bsonType": "string",
                "description": "the first name of a user must be determined"
            },
            "lastName": {
                "bsonType": "string",
                "description": "the last name of a user must be determined"
            },
            "email": {
                "bsonType": "string",
                "description": "the email address of a user must be determined",
                "uniqueItems": True
            },
            "tasks": {
                "bsonType": "array",
                "items": {
                    "bsonType": "objectId"
                }
            }
        }
    }
}


@pytest.fixture(scope="function")
def user_dao():
    """
    Create a temporary test collection with the user validator.
    Uses the correct MongoDB connection from Docker.
    Drops the collection after each test.
    """
    collection_name = f"user_test_{uuid.uuid4().hex[:6]}"
    with patch("src.util.dao.getValidator", return_value=USER_VALIDATOR):
        dao = DAO(collection_name=collection_name)

    yield dao
    try:
        dao.drop()
    except Exception:
        pass

@pytest.mark.integration
def test_create_valid_user_should_pass(user_dao):
    data = {
        "firstName": "Alice",
        "lastName": "Smith",
        "email": "alice@example.com"
    }
    result = user_dao.create(data)

    assert result is not None
    assert "_id" in result
    assert result["firstName"] == "Alice"
    assert result["lastName"] == "Smith"
    assert result["email"] == "alice@example.com"

@pytest.mark.integration
def test_create_user_missing_required_field_should_raise_error(user_dao):
    data = {
        "firstName": "Alice",
        "lastName": "Smith"
    }

    with pytest.raises(WriteError) as exc_info:
        user_dao.create(data)
    assert exc_info.value.code == 121

@pytest.mark.integration
def test_create_user_duplicate_email_should_raise_error(user_dao):
    first = {
        "firstName": "Alice",
        "lastName": "Smith",
        "email": "alice@example.com"
    }
    second = {
        "firstName": "Bob",
        "lastName": "Jones",
        "email": "alice@example.com"
    }

    user_dao.create(first)

    with pytest.raises(WriteError):
        user_dao.create(second)
        
@pytest.mark.integration
def test_create_user_wrong_type_should_raise_error(user_dao):
    data = {
        "firstName": 123,
        "lastName": "Smith",
        "email": "alice@example.com"
    }

    with pytest.raises(WriteError) as exc_info:
        user_dao.create(data)
    assert exc_info.value.code == 121


@pytest.mark.integration
def test_create_user_with_optional_tasks_array_should_pass(user_dao):
    data = {
        "firstName": "Carol",
        "lastName": "Brown",
        "email": "carol@example.com",
        "tasks": []
    }

    result = user_dao.create(data)
    assert result is not None
    assert result.get("tasks") == []


@pytest.mark.integration
def test_create_user_with_wrong_tasks_type_should_raise_error(user_dao):
    data = {
        "firstName": "Dave",
        "lastName": "Miller",
        "email": "dave@example.com",
        "tasks": "not-an-array"
    }

    with pytest.raises(WriteError) as exc_info:
        user_dao.create(data)
    assert exc_info.value.code == 121