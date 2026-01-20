from typing import List

from src.domain.models import Price
from src.infrastructure.database.repositories.price_repository import PriceRepository


class GetAllPricesUseCase:
    def __init__(self, repository: PriceRepository):
        self.repository = repository

    async def execute(self, ticker: str) -> List[Price]:
        return await self.repository.get_all_by_ticker(ticker)
