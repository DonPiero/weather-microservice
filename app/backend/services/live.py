import grpc
import aiohttp

from app.core.config import settings
from app.core.loging import logger
from app.db.models import WeatherData
from app.db.session import db
from app.db.repositories.insert_live import insert_weather_data
from app.backend import weather_pb2


async def handle_live_weather(request, context) -> weather_pb2.WeatherResponse:
    try:
        logger.debug(f"Handling live weather request for city: {request.city_name}")

        if dict(context.invocation_metadata()).get("x-api-key") != settings.grpc_api_key:
            raise PermissionError("Invalid API key")

        logger.debug("API key validated successfully.")

        city = request.city_name.strip().lower()
        if not city:
            raise ValueError("City name cannot be empty")

        logger.debug("City name validated successfully.")

        session = None
        resp = None

        try:
            params = {
                "q": city,
                "appid": settings.weather_api_key,
                "units": "metric"
            }

            logger.debug("Sending request to external weather API.")

            session = aiohttp.ClientSession()
            resp = await session.get("http://api.openweathermap.org/data/2.5/weather", params=params)

            if resp.status != 200:
                raise LookupError(f"City '{city}' not found or API returned status {resp.status}")

            logger.debug("External API request have been successful.")

            data = await resp.json()

            weather = WeatherData(
                city_name=data["name"],
                temperature=data["main"]["temp"],
                weather_description=data["weather"][0]["description"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
            )

            logger.debug(f"Parsed weather data: {weather}")

            await insert_weather_data(db, weather)

            logger.info(f"Inserted live weather data for city: {city} into the database.")

            return weather_pb2.WeatherResponse(
                city_name=weather.city_name,
                temperature=weather.temperature,
                weather_description=weather.weather_description,
                humidity=weather.humidity,
                wind_speed=weather.wind_speed or 0.0,
                timestamp=str(weather.timestamp),
            )
        except KeyError as e:
            logger.error(f"Unexpected API response format, missing key: {e}")
            context.set_code(grpc.StatusCode.DATA_LOSS)
            context.set_details("Malformed API response data.")
            return weather_pb2.WeatherResponse()
        except LookupError as e:
            logger.error(f"City not found or a different API error occurred: {e}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"City '{city}' not found or a different API error occurred.")
            return weather_pb2.WeatherResponse()
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
    except PermissionError as e:
        logger.error(f"Invalid x-api-key protection key: {e}")
        context.set_code(grpc.StatusCode.PERMISSION_DENIED)
        context.set_details("Invalid API protection key.")
        return weather_pb2.WeatherResponse()
    except ValueError as e:
        logger.error(f"Empty city name argument provided: {e}")
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        context.set_details("You must provide a non-empty city name.")
        return weather_pb2.WeatherResponse()
    except Exception as e:
        logger.critical(f"Error fetching live weather: {e}")
        context.set_code(grpc.StatusCode.UNAVAILABLE)
        context.set_details("Failed to fetch live weather from external API.")
        return weather_pb2.WeatherResponse()
