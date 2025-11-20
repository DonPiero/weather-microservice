from app.core.loging import logger
from app.db.session import db
from app.db.models.user import User
from app.db.repositories.insert_user import insert_user
from app.db.repositories.get_user import get_user
from app.core.security.password import hash_password


async def register_user(email: str, password: str) -> bool:
    try:
        logger.debug(f"Attempting to register user with email: {email}")

        existing_user = await get_user(db, email)
        if existing_user:
            raise ValueError("Email is already registered.")

        logger.debug("Email is available, proceeding with registration.")

        hashed = hash_password(password)
        if not hashed:
            raise RuntimeError("Password hashing failed.")

        logger.debug("Password hashed successfully.")

        user = User(email=email, password=hashed)
        await insert_user(db, user)

        logger.info(f"User registered successfully with email: {email}")

        return True

    except ValueError as e:
        logger.warning(f"Registration attempt with existing email: {email}. Error: {e}")
        return False
    except RuntimeError as e:
        logger.error(f"Password hashing failed during registration. Error: {e}")
        return False
    except Exception as e:
        logger.critical(f"Unexpected error during registration for {email}: {e}")
        return False
