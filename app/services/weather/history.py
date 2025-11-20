import grpc
from datetime import datetime

from app.core.config import settings
from app.core.loging import logger
from app.db.models.weather import WeatherHistory
from app.db.session import db
from app.db.repositories.get_history import get_weather_history
from app.services.rpc import weather_pb2


async def handle_weather_history(request, context) -> weather_pb2.WeatherHistoryResponse:
    try:
        logger.debug(f"Handling weather history request for city: {request.city_name}")

        email = dict(context.invocation_metadata()).get("user-email")
        if not email or dict(context.invocation_metadata()).get("x-api-key") != settings.grpc_api_key:
            raise PermissionError("User not authorized or invalid API key.")

        logger.debug("API key and user email validated successfully.")

        city = request.city_name.strip().lower()
        if not city:
            raise ValueError("City name cannot be empty")

        logger.debug("City name validated successfully.")

        weather_history_parameters = WeatherHistory(
            email=email,
            city_name=city,
            start_time=datetime.fromisoformat(request.start_time),
            end_time=datetime.fromisoformat(request.end_time),
        )

        readings = await get_weather_history(db, weather_history_parameters)

        logger.info(f"Fetched {len(readings)} weather readings from the database.")

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

    except PermissionError as e:
        logger.error(f"Email missing or wrong API key: {e}")
        context.set_code(grpc.StatusCode.PERMISSION_DENIED)
        context.set_details("Missing email or invalid API protection key.")
        return weather_pb2.WeatherHistoryResponse()
    except ValueError as e:
        logger.error(f"City name or dates are invalid: {e}")
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        context.set_details("You must provide a non-empty city name and valid formatted dates.")
        return weather_pb2.WeatherHistoryResponse()
    except ConnectionError as e:
        logger.error(f"Database connection failed: {e}")
        context.set_code(grpc.StatusCode.UNAVAILABLE)
        context.set_details("Database connection issue.")
        return weather_pb2.WeatherHistoryResponse()
    except Exception as e:
        logger.critical(f"Error fetching weather history: {e}")
        context.set_code(grpc.StatusCode.UNAVAILABLE)
        context.set_details("Failed to fetch weather history from the database.")
        return weather_pb2.WeatherHistoryResponse()
