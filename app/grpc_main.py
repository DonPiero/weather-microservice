import asyncio

from app.services.rpc.server import serve
from app.core.loging import logger

try:
    asyncio.run(serve())
except asyncio.CancelledError as e:
    logger.warning(f"Asyncio run got cancelled: {e}")
except OSError as e:
    logger.error(f"System or network error: {e}")
except Exception as e:
    logger.critical(f"Fatal error encountered: {e}")