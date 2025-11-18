import grpc

from app.core.loging import logger
from app.grpc import weather_pb2_grpc, weather_pb2
from app.grpc.services.live import handle_live_weather
from app.grpc.services.history import handle_weather_history


class WeatherServiceServicer(weather_pb2_grpc.WeatherServiceServicer):
    async def GetWeather(self, request, context):
        try:
            return await handle_live_weather(request, context)
        except Exception as e:
            logger.error(f"Unhandled error while getting the live weather: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error occurred.")
            return weather_pb2.WeatherResponse()

    async def GetWeatherHistory(self, request, context):
        try:
            return await handle_weather_history(request, context)
        except Exception as e:
            logger.error(f"Unhandled error while getting the weather history: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error occurred.")
            return weather_pb2.WeatherHistoryResponse()
