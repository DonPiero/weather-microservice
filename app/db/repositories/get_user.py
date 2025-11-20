from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.models.user import User


async def get_user(db: AsyncIOMotorDatabase, email: str) -> User | None:
    data = await db.users.find_one({"email": email})

    return User(**{k: v for k, v in data.items() if k != "_id"}) if data else None
