from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.models import WeatherData
from datetime import datetime
from typing import List


async def get_weather_history(db: AsyncIOMotorDatabase, city_name: str, start_time: datetime, end_time: datetime) -> List[WeatherData]:
    results = await db.weather_data.find({
        "city_name": city_name,
        "timestamp": {"$gte": start_time, "$lte": end_time}
    }).sort("timestamp", 1).to_list(length=None)

    return [WeatherData(**{k: v for k, v in doc.items() if k != "_id"}) for doc in results]
