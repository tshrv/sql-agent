import asyncpg
from typing import List, Dict, Any
from app.settings import Settings


class DatabaseClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.pool: asyncpg.Pool | None = None

    async def connect(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                user=self.settings.postgres_user,
                password=self.settings.postgres_password,
                database=self.settings.postgres_db,
                host=self.settings.postgres_host,
                port=self.settings.postgres_port,
            )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def execute_query(self, query: str) -> List[Dict[str, Any]]:
        if self.pool is None:
            await self.connect()
        records = await self.pool.fetch(query)
        return [dict(record) for record in records]