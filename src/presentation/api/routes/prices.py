from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from src.application.use_cases.get_all_prices import GetAllPricesUseCase
from src.application.use_cases.get_last_price import GetLastPriceUseCase
from src.application.use_cases.get_price_by_date import GetPriceByDateUseCase
from src.infrastructure.database.repositories.price_repository import PriceRepository
from src.presentation.schemas.price_schemas import PriceResponse

router = APIRouter()


async def get_repository(request: Request) -> PriceRepository:
    db = request.app.state.db
    return PriceRepository(db)


@router.get("/all", response_model=List[PriceResponse])
async def get_all_prices(ticker: str, repository: PriceRepository = Depends(get_repository)):
    use_case = GetAllPricesUseCase(repository)
    prices = await use_case.execute(ticker)
    result = []
    for price in prices:
        result.append(PriceResponse(
            ticker=price.ticker,
            price=price.price,
            timestamp=price.timestamp
        ))
    return result


@router.get("/last", response_model=PriceResponse)
async def get_last_price(ticker: str, repository: PriceRepository = Depends(get_repository)):
    use_case = GetLastPriceUseCase(repository)
    price = await use_case.execute(ticker)
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    return PriceResponse(ticker=price.ticker, price=price.price, timestamp=price.timestamp)


@router.get("/by-date", response_model=PriceResponse)
async def get_price_by_date(
        ticker: str,
        date: int,
        repository: PriceRepository = Depends(get_repository)
):
    use_case = GetPriceByDateUseCase(repository)
    price = await use_case.execute(ticker, date)
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    return PriceResponse(ticker=price.ticker, price=price.price, timestamp=price.timestamp)
