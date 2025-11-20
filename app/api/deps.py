import grpc
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.api.errors import error_401, error_404, error_500, error_403
from app.services.rpc import weather_pb2_grpc
from app.core.security.access import decode_access_token
from app.db.models.user import User
from app.db.repositories.get_user import get_user
from app.db.session import db


user_token = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_user_from_token(token: str = Depends(user_token)) -> User | None:
    try:
        payload = decode_access_token(token)
        if not payload:
            error_401("Invalid or expired token.")

        email = payload.get("sub")
        if not email:
            error_401("Email field missing.")

        user = await get_user(db, email)
        if not user:
            error_404("User not found.")

        return user

    except HTTPException:
        raise
    except Exception as e:
        error_500(f"Error retrieving user from token: {e}")


async def get_connection_to_grpc() -> weather_pb2_grpc.WeatherServiceStub | None:
    try:
        return weather_pb2_grpc.WeatherServiceStub(grpc.aio.insecure_channel("weather_grpc:50051"))

    except Exception as e:
        error_500(f"Error creating gRPC connection: {e}")
