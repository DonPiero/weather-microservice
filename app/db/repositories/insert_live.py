from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.models import WeatherData


async def insert_weather_data(db: AsyncIOMotorDatabase, data: WeatherData) -> None:
    await db.weather_data.insert_one(data.model_dump())

    return None