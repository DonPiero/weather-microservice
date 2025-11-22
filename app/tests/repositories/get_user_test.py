import pytest
from unittest.mock import AsyncMock

from app.db.models.user import User
from app.db.repositories import get_user


@pytest.mark.asyncio
async def test_get_user_found():
    fake_db = AsyncMock()
    fake_db.users = AsyncMock()
    fake_db.users.find_one = AsyncMock(
        return_value={"email": "u@example.com", "password": "hashed123"}
    )

    result = await get_user.get_user(fake_db, "u@example.com")

    fake_db.users.find_one.assert_awaited_once_with({"email": "u@example.com"})
    assert isinstance(result, User)
    assert result.email == "u@example.com"
    assert result.password == "hashed123"


@pytest.mark.asyncio
async def test_get_user_not_found():
    fake_db = AsyncMock()
    fake_db.users = AsyncMock()
    fake_db.users.find_one = AsyncMock(return_value=None)

    result = await get_user.get_user(fake_db, "ghost@example.com")

    fake_db.users.find_one.assert_awaited_once_with({"email": "ghost@example.com"})
    assert result is None


@pytest.mark.asyncio
async def test_get_user_db_error(monkeypatch):
    fake_db = AsyncMock()
    fake_db.users = AsyncMock()
    fake_db.users.find_one = AsyncMock(side_effect=RuntimeError("DB failure"))

    with pytest.raises(RuntimeError):
        await get_user.get_user(fake_db, "ghost@example.com")
