import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.db.models.weather import WeatherData
from app.services.weather import history
from app.services.rpc import weather_pb2


@pytest.mark.asyncio
async def test_handle_weather_history_success(monkeypatch):
    fake_context = MagicMock()
    fake_context.invocation_metadata.return_value = [
        ("x-api-key", "valid-key"),
        ("user-email", "user@example.com"),
    ]

    monkeypatch.setattr(history.settings, "grpc_api_key", "valid-key")

    fake_readings = [
        WeatherData(
            email="user@example.com",
            city_name="london",
            temperature=19.5,
            weather_description="clear sky",
            humidity=55,
            wind_speed=4.0,
        )
    ]

    with patch("app.services.weather.history.get_weather_history", new=AsyncMock(return_value=fake_readings)):
        result = await history.handle_weather_history(
            weather_pb2.WeatherHistoryRequest(
                city_name="London",
                start_time="2025-11-20T00:00:00",
                end_time="2025-11-21T00:00:00",
            ),
            fake_context,
        )

    assert isinstance(result, weather_pb2.WeatherHistoryResponse)
    assert len(result.readings) == 1
    r = result.readings[0]
    assert r.city_name == "london"
    assert pytest.approx(r.temperature, 0.1) == 19.5
    assert r.weather_description == "clear sky"
    assert pytest.approx(r.humidity, 0.1) == 55.0


@pytest.mark.asyncio
async def test_handle_weather_history_invalid_api_key(monkeypatch):
    fake_context = MagicMock()
    fake_context.invocation_metadata.return_value = [
        ("x-api-key", "wrong-key"),
        ("user-email", "user@example.com"),
    ]

    monkeypatch.setattr(history.settings, "grpc_api_key", "valid-key")

    result = await history.handle_weather_history(
        weather_pb2.WeatherHistoryRequest(
            city_name="London",
            start_time="2025-11-20T00:00:00",
            end_time="2025-11-21T00:00:00",
        ),
        fake_context,
    )

    assert isinstance(result, weather_pb2.WeatherHistoryResponse)
    assert len(result.readings) == 0


@pytest.mark.asyncio
async def test_handle_weather_history_empty_city(monkeypatch):
    fake_context = MagicMock()
    fake_context.invocation_metadata.return_value = [
        ("x-api-key", "valid-key"),
        ("user-email", "user@example.com"),
    ]

    monkeypatch.setattr(history.settings, "grpc_api_key", "valid-key")

    result = await history.handle_weather_history(
        weather_pb2.WeatherHistoryRequest(
            city_name="",
            start_time="2025-11-20T00:00:00",
            end_time="2025-11-21T00:00:00",
        ),
        fake_context,
    )

    assert isinstance(result, weather_pb2.WeatherHistoryResponse)
