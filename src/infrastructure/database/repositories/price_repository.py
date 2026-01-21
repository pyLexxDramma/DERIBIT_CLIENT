from typing import List, Optional

from src.domain.models import Price
from src.infrastructure.database.connection import Database


class PriceRepository:
    def __init__(self, db: Database):
        self.db = db

    async def create_table_if_not_exists(self):
        pool = await self.db.get_pool()
        async with pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS prices (
                    id SERIAL PRIMARY KEY,
                    ticker VARCHAR(10) NOT NULL,
                    price DECIMAL(20, 8) NOT NULL,
                    timestamp BIGINT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_ticker_timestamp 
                ON prices(ticker, timestamp DESC)
            """)

    async def save(self, price: Price) -> None:
        pool = await self.db.get_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO prices (ticker, price, timestamp) VALUES ($1, $2, $3)",
                price.ticker, price.price, price.timestamp
            )

    async def get_all_by_ticker(self, ticker: str) -> List[Price]:
        pool = await self.db.get_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT ticker, price, timestamp FROM prices WHERE ticker = $1 ORDER BY timestamp DESC",
                ticker
            )
            price_list = []
            for row in rows:
                price_list.append(Price(
                    ticker=row["ticker"],
                    price=float(row["price"]),
                    timestamp=row["timestamp"]
                ))
            return price_list

    async def get_last_by_ticker(self, ticker: str) -> Optional[Price]:
        pool = await self.db.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT ticker, price, timestamp FROM prices WHERE ticker = $1 ORDER BY timestamp DESC LIMIT 1",
                ticker
            )
            if row:
                return Price(
                    ticker=row["ticker"],
                    price=float(row["price"]),
                    timestamp=row["timestamp"]
                )
            return None

    async def get_by_ticker_and_date(self, ticker: str, timestamp: int) -> Optional[Price]:
        pool = await self.db.get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT ticker, price, timestamp 
                FROM prices 
                WHERE ticker = $1 AND timestamp = $2
                LIMIT 1
                """,
                ticker, timestamp
            )
            if row:
                return Price(
                    ticker=row["ticker"],
                    price=float(row["price"]),
                    timestamp=row["timestamp"]
                )
            return None
