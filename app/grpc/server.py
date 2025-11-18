import grpc
from concurrent import futures
from app.grpc import weather_pb2_grpc
from app.db.session import client
from app.core.loging import logger
from app.grpc.servicer import WeatherServiceServicer


async def serve():
    server = None
    try:
        server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
        weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherServiceServicer(), server)
        server.add_insecure_port("[::]:50051")
        logger.info("Attempting to start the server.")
        await server.start()
        logger.info("Server started successfully.")
        await server.wait_for_termination()
        logger.info("Server stopped successfully.")

    except KeyboardInterrupt:
        logger.info("Server stopped manually.")
    except Exception as e:

        logger.error(f"Failed to start the server, because: {e}")

    finally:
        await server.stop(0)
        client.close()
