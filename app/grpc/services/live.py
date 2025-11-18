import grpc
import aiohttp

from app.core.config import settings
from app.core.loging import logger
from app.db.models import WeatherData
from app.db.session import db
from app.db.repositories import insert_weather_data
from app.grpc import weather_pb2


async def handle_live_weather(request, context) -> weather_pb2.WeatherResponse:
    try:
        if dict(context.invocation_metadata()).get("x-api-key") != settings.grpc_api_key:
            logger.info("Invalid x-api-key protection key.")
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Invalid API protection key.")
            return weather_pb2.WeatherResponse()

        city = request.city_name.strip()
        if not city:
            logger.info("Empty city name argument provided.")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("You must provide a non-empty city name.")
            return weather_pb2.WeatherResponse()

        session = None
        resp = None

        try:
            params = {
                "q": city,
                "appid": settings.openweather_api_key,
                "units": "metric"
            }
            session = aiohttp.ClientSession()
            resp = await session.get("http://api.openweathermap.org/data/2.5/weather", params=params)

            if resp.status != 200:
                logger.info("City not found or a different API error occurred.")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"City '{city}' not found or a different API error occurred.")
                return weather_pb2.WeatherResponse()

            data = await resp.json()

            weather = WeatherData(
                city_name=data["name"],
                temperature=data["main"]["temp"],
                weather_description=data["weather"][0]["description"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
            )

            await insert_weather_data(db, weather)

            return weather_pb2.WeatherResponse(
                city_name=weather.city_name,
                temperature=weather.temperature,
                weather_description=weather.weather_description,
                humidity=weather.humidity,
                wind_speed=weather.wind_speed or 0.0,
                timestamp=str(weather.timestamp),
            )

        except Exception as e:
            logger.error(f"Error processing weather data: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error processing weather data.")
            return weather_pb2.WeatherResponse()

        finally:
            if resp:
                await resp.release()
            if session:
                await session.close()

    except Exception as e:
        logger.error(f"Error fetching live weather: {e}")
        context.set_code(grpc.StatusCode.UNAVAILABLE)
        context.set_details("Failed to fetch live weather from external API.")
        return weather_pb2.WeatherResponse()
