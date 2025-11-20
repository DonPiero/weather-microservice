from app.core.loging import logger
from app.db.session import db
from app.db.repositories.get_user import get_user
from app.core.security.password import verify_password
from app.core.security.access import create_access_token


async def login_user(email: str, password: str) -> str | None:
    try:
        logger.debug(f"Login attempt for email: {email}")

        user = await get_user(db, email)
        if not user:
            raise ValueError("User not found.")

        logger.debug("User found, verifying password.")

        valid = verify_password(password, user.password)
        if not valid:
            raise PermissionError("Invalid credentials.")

        logger.debug("Password verified successfully.")

        token = create_access_token({"sub": user.email})
        if not token:
            raise RuntimeError("Token generation failed.")

        logger.info(f"User logged in successfully: {email}")
        return token

    except ValueError as e:
        logger.warning(f"Login failed for {email}: {e}")
        return None
    except PermissionError as e:
        logger.warning(f"Incorrect password for {email}: {e}")
        return None
    except RuntimeError as e:
        logger.error(f"Token generation failed for {email}: {e}")
        return None
    except Exception as e:
        logger.critical(f"Unexpected error during login for {email}: {e}")
        return None
