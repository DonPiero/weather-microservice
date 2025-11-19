import asyncio
from app.backend.server import serve
from app.core.loging import logger

try:
    logger.info("Starting Weather-Microservice.")
    asyncio.run(serve())
except KeyboardInterrupt:
    logger.info("Weather-Microservice stopped manually.")
except asyncio.CancelledError as e:
    logger.warning(f"Asyncio run got cancelled: {e}")
except OSError as e:
    logger.error(f"System or network error: {e}")
except Exception as e:
    logger.critical(f"Fatal error encountered: {e}")