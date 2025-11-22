import pytest
from unittest.mock import AsyncMock
from pydantic import ValidationError
from app.db.repositories import insert_user
from app.db.models.user import User


@pytest.mark.asyncio
async def test_insert_user_success():
    fake_db = AsyncMock()
    fake_db.users = AsyncMock()
    fake_db.users.insert_one = AsyncMock(return_value={"inserted_id": "abc123"})

    user = User(email="newuser@example.com", password="hashed123")

    result = await insert_user.insert_user(fake_db, user)

    fake_db.users.insert_one.assert_awaited_once()
    args, kwargs = fake_db.users.insert_one.call_args
    inserted_doc = args[0]
    assert inserted_doc["email"] == "newuser@example.com"
    assert inserted_doc["password"] == "hashed123"
    assert result is None


@pytest.mark.asyncio
async def test_insert_user_invalid_email():
    with pytest.raises(ValidationError):
        User(email="not-an-email", password="hashed123")


@pytest.mark.asyncio
async def test_insert_user_db_error():
    fake_db = AsyncMock()
    fake_db.users = AsyncMock()
    fake_db.users.insert_one = AsyncMock(side_effect=RuntimeError("DB write failure"))

    user = User(email="fail@example.com", password="hash")

    with pytest.raises(RuntimeError):
        await insert_user.insert_user(fake_db, user)
