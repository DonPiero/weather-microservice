import pytest
from unittest.mock import AsyncMock
from app.services.authentication import login


@pytest.mark.asyncio
async def test_login_user_success(monkeypatch):
    fake_user = type("User", (), {"email": "user@example.com", "password": "hashedpass"})

    monkeypatch.setattr(login, "get_user", AsyncMock(return_value=fake_user))
    monkeypatch.setattr(login, "verify_password", lambda plain, hashed: True)
    monkeypatch.setattr(login, "create_access_token", lambda payload: "fake-jwt")

    result = await login.login_user("user@example.com", "password123")

    assert result == "fake-jwt"


@pytest.mark.asyncio
async def test_login_user_user_not_found(monkeypatch):
    monkeypatch.setattr(login, "get_user", AsyncMock(return_value=None))
    result = await login.login_user("notfound@example.com", "password123")
    assert result is None


@pytest.mark.asyncio
async def test_login_user_invalid_password(monkeypatch):
    fake_user = type("User", (), {"email": "user@example.com", "password": "hashedpass"})
    monkeypatch.setattr(login, "get_user", AsyncMock(return_value=fake_user))
    monkeypatch.setattr(login, "verify_password", lambda plain, hashed: False)

    result = await login.login_user("user@example.com", "wrongpassword")
    assert result is None
