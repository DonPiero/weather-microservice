from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.models.weather import WeatherData, WeatherHistory
from typing import List


async def get_weather_history(db: AsyncIOMotorDatabase, weather_history_parameters: WeatherHistory) -> List[WeatherData]:
    results = await db.weather_data.find({
        "email": weather_history_parameters.email,
        "city_name": weather_history_parameters.city_name,
        "timestamp": {"$gte": weather_history_parameters.start_time, "$lte": weather_history_parameters.end_time}
    }).sort("timestamp", 1).to_list(length=None)

    return [WeatherData(**{k: v for k, v in doc.items() if k != "_id"}) for doc in results]
