import os
from typing import Optional

import asyncpg


class Database:
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "postgresql://user:password@localhost:5432/deribit_db"
        )
        self._pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self.database_url)

    async def close(self):
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def get_pool(self) -> asyncpg.Pool:
        if self._pool is None:
            await self.connect()
        return self._pool
