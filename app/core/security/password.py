from passlib.context import CryptContext

from app.core.loging import logger

hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str | None:
    try:
        return hasher.hash(password)
    except Exception as e:
        logger.error(f"Password hashing failed: {e}")
        return None

def verify_password(plain_password: str, hashed_password: str) -> bool | None:
    try:
        return hasher.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification failed: {e}")
        return None