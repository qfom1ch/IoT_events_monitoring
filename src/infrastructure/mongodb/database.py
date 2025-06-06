from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]


async def create_indexes() -> None:
    await db['devices'].create_index('id', unique=True)


async def connect_and_init_db() -> None:
    await create_indexes()


async def close_db_connection() -> None:
    client.close()
