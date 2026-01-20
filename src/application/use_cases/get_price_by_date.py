from typing import Optional
from src.domain.models import Price
from src.infrastructure.database.repositories.price_repository import PriceRepository


class GetPriceByDateUseCase:
    def __init__(self, repository: PriceRepository):
        self.repository = repository

    async def execute(self, ticker: str, timestamp: int) -> Optional[Price]:
        return await self.repository.get_by_ticker_and_date(ticker, timestamp)
