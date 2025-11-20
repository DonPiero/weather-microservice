from app.api.routers.authentication import login, register
from app.api.routers.weather import history, live
from app.core.loging import logger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    logger.info("Starting the FastAPI server.")
    app = FastAPI(title="Weather GRPC Service")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(login.router)
    app.include_router(register.router)
    app.include_router(live.router)
    app.include_router(history.router)

    logger.info("FastAPI server started successfully.")

except OSError as e:
    logger.error(f"System or network error: {e}")
except Exception as e:
    logger.critical(f"Fatal error encountered: {e}")