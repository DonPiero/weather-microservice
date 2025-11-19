import grpc
from concurrent import futures
from app.backend import weather_pb2_grpc
from app.db.session import client
from app.core.loging import logger
from app.backend.servicer import WeatherServiceServicer


async def serve():
    server = None
    try:
        server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
        weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherServiceServicer(), server)
        server.add_insecure_port("[::]:50051")
        logger.info("Starting the server.")
        await server.start()
        logger.debug("Server started successfully.")
        await server.wait_for_termination()
        logger.debug("Server stopped successfully.")

    except KeyboardInterrupt:
        logger.info("Server stopped manually.")
    except grpc.RpcError as e:
        logger.error(f"GRPC error occurred: {e}")
    except OSError as e:
        logger.error(f"System or network error while starting the server: {e}")
    except Exception as e:
        logger.critical(f"Failed to start the server, because: {e}")

    finally:
        await server.stop(0)
        client.close()
