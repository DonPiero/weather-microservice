from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt

from app.core.config import settings
from app.core.loging import logger


def create_access_token(credentials: dict) -> str | None:
    try:
        to_encode = credentials.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiration_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    except Exception as e:
        logger.error(f"Token creation failed: {e}")
        return None

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except Exception as e:
        logger.error(f"Unexpected error decoding token: {e}")
        return None
