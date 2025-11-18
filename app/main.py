import asyncio
from app.grpc.server import serve
from app.core.loging import logger

try:
    logger.info("Starting Weather-Microservice.")
    asyncio.run(serve())
except KeyboardInterrupt:
    logger.info("Weather-Microservice stopped manually.")
except Exception as e:
    logger.error(f"Fatal error encountered: {e}")