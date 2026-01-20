from typing import Optional

from src.domain.models import Price
from src.infrastructure.database.repositories.price_repository import PriceRepository


class GetLastPriceUseCase:
    def __init__(self, repository: PriceRepository):
        self.repository = repository

    async def execute(self, ticker: str) -> Optional[Price]:
        return await self.repository.get_last_by_ticker(ticker)
