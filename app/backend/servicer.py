import grpc

from app.core.loging import logger
from app.backend import weather_pb2_grpc, weather_pb2
from app.backend.services.live import handle_live_weather
from app.backend.services.history import handle_weather_history


class WeatherServiceServicer(weather_pb2_grpc.WeatherServiceServicer):
    async def GetWeather(self, request, context):
        try:
            logger.debug(f"Received GetWeather request.")
            return await handle_live_weather(request, context)
        except grpc.RpcError as e:
            logger.error(f"GRPC error: {e}")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details("GRPC error occurred.")
            return weather_pb2.WeatherResponse()
        except ValueError as e:
            logger.error(f"Value error: {e}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid value provided.")
            return weather_pb2.WeatherResponse()
        except Exception as e:
            logger.critical(f"Unhandled error while getting the live weather: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error occurred.")
            return weather_pb2.WeatherResponse()

    async def GetWeatherHistory(self, request, context):
        try:
            logger.debug("Received GetWeatherHistory request.")
            return await handle_weather_history(request, context)
        except grpc.RpcError as e:
            logger.error(f"GRPC error: {e}")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details("GRPC error occurred.")
            return weather_pb2.WeatherHistoryResponse()
        except ValueError as e:
            logger.error(f"Value error: {e}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid value provided.")
            return weather_pb2.WeatherHistoryResponse()
        except Exception as e:
            logger.critical(f"Unhandled error while getting the weather history: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error occurred.")
            return weather_pb2.WeatherHistoryResponse()
