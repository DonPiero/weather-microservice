import grpc
from datetime import datetime

from app.core.config import settings
from app.core.loging import logger
from app.db.session import db
from app.db.repositories import get_weather_history
from app.grpc import weather_pb2


async def handle_weather_history(request, context) -> weather_pb2.WeatherHistoryResponse:
    try:
        if dict(context.invocation_metadata()).get("x-api-key") != settings.grpc_api_key:
            logger.info("Invalid x-api-key protection key.")
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Invalid API protection key.")
            return weather_pb2.WeatherHistoryResponse()

        city = request.city_name.strip()
        if not city:
            logger.info("Empty city name argument provided.")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("You must provide a non-empty city name.")
            return weather_pb2.WeatherHistoryResponse()

        readings = await get_weather_history(db,
                                             city,
                                             datetime.fromisoformat(request.start_time),
                                             datetime.fromisoformat(request.end_time))

        return weather_pb2.WeatherHistoryResponse(
            readings=[
                weather_pb2.WeatherResponse(
                    city_name=r.city_name,
                    temperature=r.temperature,
                    weather_description=r.weather_description,
                    humidity=r.humidity,
                    wind_speed=r.wind_speed or 0.0,
                    timestamp=str(r.timestamp),
                )
                for r in readings
            ]
        )

    except Exception as e:
        logger.error(f"Error fetching weather history: {e}")
        context.set_code(grpc.StatusCode.UNAVAILABLE)
        context.set_details("Failed to fetch weather history from the database.")
        return weather_pb2.WeatherHistoryResponse()
