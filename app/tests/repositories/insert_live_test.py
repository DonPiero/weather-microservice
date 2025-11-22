import pytest
from unittest.mock import AsyncMock
from pydantic import ValidationError
from app.db.repositories import insert_live
from app.db.models.weather import WeatherData


@pytest.mark.asyncio
async def test_insert_weather_data_valid(monkeypatch):
    fake_db = AsyncMock()
    fake_db.weather_data = AsyncMock()
    fake_db.weather_data.insert_one = AsyncMock(return_value={"inserted_id": "12345"})

    weather = WeatherData(
        email="user@example.com",
        city_name="london",
        temperature=19.5,
        weather_description="clear sky",
        humidity=55,
        wind_speed=4.0,
    )

    result = await insert_live.insert_weather_data(fake_db, weather)

    fake_db.weather_data.insert_one.assert_awaited_once()
    args, kwargs = fake_db.weather_data.insert_one.call_args
    inserted_doc = args[0]

    assert inserted_doc["city_name"] == "london"
    assert inserted_doc["temperature"] == 19.5
    assert "timestamp" in inserted_doc
    assert result is None


@pytest.mark.asyncio
async def test_insert_weather_data_invalid_email():
    with pytest.raises(ValidationError):
        WeatherData(
            email="not-an-email",
            city_name="london",
            temperature=19.5,
            weather_description="clear sky",
            humidity=55,
        )


@pytest.mark.asyncio
async def test_insert_weather_data_missing_fields(monkeypatch):
    with pytest.raises(ValidationError):
        WeatherData(
            email="user@example.com",
            city_name="london",
            weather_description="clear sky",
        )