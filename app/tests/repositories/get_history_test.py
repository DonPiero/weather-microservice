import pytest
from unittest.mock import MagicMock, AsyncMock
from pydantic import ValidationError
from app.db.repositories import get_history
from app.db.models.weather import WeatherHistory


@pytest.mark.asyncio
async def test_get_weather_history_valid():
    fake_cursor = MagicMock()
    fake_cursor.sort.return_value = fake_cursor
    fake_cursor.to_list = AsyncMock(return_value=[
        {
            "email": "user@example.com",
            "city_name": "london",
            "temperature": 20.1,
            "weather_description": "cloudy",
            "humidity": 60,
            "wind_speed": 3.5,
            "timestamp": "2025-11-21T00:00:00",
        }
    ])

    fake_db = MagicMock()
    fake_db.weather_data.find.return_value = fake_cursor

    params = WeatherHistory(
        email="user@example.com",
        city_name="london",
        start_time="2025-11-20T00:00:00",
        end_time="2025-11-22T00:00:00",
    )

    result = await get_history.get_weather_history(fake_db, params)

    fake_db.weather_data.find.assert_called_once()
    fake_cursor.sort.assert_called_once_with("timestamp", 1)
    fake_cursor.to_list.assert_awaited_once()
    assert isinstance(result, list)
    assert hasattr(result[0], "city_name")
    assert result[0].city_name == "london"
    assert hasattr(result[0], "temperature")
    assert result[0].temperature == 20.1


@pytest.mark.asyncio
async def test_get_weather_history_invalid_dates():
    fake_cursor = MagicMock()
    fake_cursor.sort.return_value = fake_cursor
    fake_cursor.to_list = AsyncMock(return_value=[])

    fake_db = MagicMock()
    fake_db.weather_data.find.return_value = fake_cursor

    params = WeatherHistory(
        email="user@example.com",
        city_name="london",
        start_time="2025-11-25T00:00:00",
        end_time="2025-11-20T00:00:00",
    )

    result = await get_history.get_weather_history(fake_db, params)

    fake_db.weather_data.find.assert_called_once()
    fake_cursor.sort.assert_called_once()
    fake_cursor.to_list.assert_awaited_once()
    assert result == []


@pytest.mark.asyncio
async def test_get_weather_history_invalid_email():
    with pytest.raises(ValidationError):
        WeatherHistory(
            email="not-an-email",
            city_name="london",
            start_time="2025-11-20T00:00:00",
            end_time="2025-11-21T00:00:00",
        )
