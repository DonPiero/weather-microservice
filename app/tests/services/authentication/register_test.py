import pytest
from unittest.mock import AsyncMock
from app.services.authentication import register


@pytest.mark.asyncio
async def test_register_user_success(monkeypatch):
    monkeypatch.setattr(register, "get_user", AsyncMock(return_value=None))
    monkeypatch.setattr(register, "hash_password", lambda pwd: "hashed_pass")
    monkeypatch.setattr(register, "insert_user", AsyncMock(return_value=None))

    result = await register.register_user("newuser@example.com", "password123")
    assert result is True


@pytest.mark.asyncio
async def test_register_user_existing_email(monkeypatch):
    fake_user = type("User", (), {"email": "existing@example.com"})
    monkeypatch.setattr(register, "get_user", AsyncMock(return_value=fake_user))

    result = await register.register_user("existing@example.com", "password123")
    assert result is False


@pytest.mark.asyncio
async def test_register_user_hash_failure(monkeypatch):
    monkeypatch.setattr(register, "get_user", AsyncMock(return_value=None))
    monkeypatch.setattr(register, "hash_password", lambda pwd: None)

    result = await register.register_user("user@example.com", "password123")
    assert result is False
