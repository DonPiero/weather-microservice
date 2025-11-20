from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.models.user import User


async def insert_user(db: AsyncIOMotorDatabase, user: User) -> None:
    await db.users.insert_one(user.model_dump())

    return None