from celery import Celery
from src.infrastructure.external.deribit_client import DeribitClient
from src.infrastructure.database.connection import Database
from src.infrastructure.database.repositories.price_repository import PriceRepository
import os


celery_app = Celery(
    "deribit_client",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)


@celery_app.task
def fetch_prices():
    import asyncio
    
    async def _fetch():
        db = Database()
        client = DeribitClient()
        repo = PriceRepository(db)
        
        try:
            await db.connect()
            await repo.create_table_if_not_exists()
            
            btc_price = await client.get_btc_price()
            if btc_price:
                await repo.save(btc_price)
            
            eth_price = await client.get_eth_price()
            if eth_price:
                await repo.save(eth_price)
        finally:
            await client.close()
            await db.close()
    
    asyncio.run(_fetch())


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, fetch_prices.s(), name='fetch prices every minute')
