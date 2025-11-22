import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.weather import live
from app.services.rpc import weather_pb2

@pytest.mark.asyncio
async def test_handle_live_weather_success(monkeypatch):
    fake_context = MagicMock()
    fake_context.invocation_metadata.return_value = [
        ("x-api-key", "valid-key"), ("user-email", "user@example.com")
    ]

    monkeypatch.setattr(live.settings, "grpc_api_key", "valid-key")
    monkeypatch.setattr(live.settings, "weather_api_key", "fake-weather-key")

    fake_response = AsyncMock()
    fake_response.status = 200
    fake_response.json.return_value = {
        "name": "London",
        "main": {"temp": 20.0, "humidity": 50},
        "weather": [{"description": "clear"}],
        "wind": {"speed": 3.5},
    }

    fake_session = AsyncMock()
    fake_session.get.return_value = fake_response

    with patch("app.services.weather.live.aiohttp.ClientSession", return_value=fake_session):
        with patch("app.services.weather.live.insert_weather_data", new=AsyncMock()):
            result = await live.handle_live_weather(weather_pb2.WeatherRequest(city_name="London"), fake_context)

    assert isinstance(result, weather_pb2.WeatherResponse)
    assert result.city_name == "london"
    assert pytest.approx(result.temperature, 0.1) == 20.0
    assert result.weather_description == "clear"

@pytest.mark.asyncio
async def test_handle_live_weather_invalid_api_key(monkeypatch):
    fake_context = MagicMock()
    fake_context.invocation_metadata.return_value = [
        ("x-api-key", "wrong-key"), ("user-email", "user@example.com")
    ]
    monkeypatch.setattr(live.settings, "grpc_api_key", "valid-key")

    result = await live.handle_live_weather(weather_pb2.WeatherRequest(city_name="Paris"), fake_context)
    assert isinstance(result, weather_pb2.WeatherResponse)
    assert result.city_name == ""

@pytest.mark.asyncio
async def test_handle_live_weather_empty_city(monkeypatch):
    fake_context = MagicMock()
    fake_context.invocation_metadata.return_value = [
        ("x-api-key", "valid-key"), ("user-email", "user@example.com")
    ]
    monkeypatch.setattr(live.settings, "grpc_api_key", "valid-key")

    result = await live.handle_live_weather(weather_pb2.WeatherRequest(city_name=""), fake_context)
    assert isinstance(result, weather_pb2.WeatherResponse)
