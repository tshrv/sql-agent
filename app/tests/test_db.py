import asyncio
from .settings import settings
from .db import DatabaseClient


async def test():
    db_client = DatabaseClient(settings)
    await db_client.connect()
    try:
        result = await db_client.execute_query("SELECT 1 as test")
        print("Query result:", result)
    finally:
        await db_client.disconnect()


if __name__ == "__main__":
    asyncio.run(test())