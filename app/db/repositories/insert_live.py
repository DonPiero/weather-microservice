from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.models.weather import WeatherData


async def insert_weather_data(db: AsyncIOMotorDatabase, live_weather: WeatherData) -> None:
    await db.weather_data.insert_one(live_weather.model_dump())

    return None