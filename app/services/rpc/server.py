import grpc
from app.services.rpc import weather_pb2_grpc
from app.db.session import client
from app.core.loging import logger
from app.services.rpc.servicer import WeatherServiceServicer


async def serve():
    server = None
    try:
        server = grpc.aio.server()
        weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherServiceServicer(), server)
        server.add_insecure_port("[::]:50051")
        logger.info("Starting the GRPC server.")
        await server.start()
        logger.info("GRPC server started successfully.")
        await server.wait_for_termination()

    except grpc.RpcError as e:
        logger.error(f"GRPC error occurred: {e}")
    except OSError as e:
        logger.error(f"System or network error while starting the server: {e}")
    except Exception as e:
        logger.critical(f"Failed to start the server, because: {e}")

    finally:
        await server.stop(0)
        client.close()
