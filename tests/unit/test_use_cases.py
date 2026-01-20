import pytest
from unittest.mock import AsyncMock, MagicMock

from src.application.use_cases.get_all_prices import GetAllPricesUseCase
from src.application.use_cases.get_last_price import GetLastPriceUseCase
from src.application.use_cases.get_price_by_date import GetPriceByDateUseCase
from src.domain.models import Price


@pytest.mark.asyncio
async def test_get_all_prices_returns_list():
    # мокаем репозиторий, чтобы не лезть в БД
    mock_repo = MagicMock()
    mock_repo.get_all_by_ticker = AsyncMock(return_value=[
        Price(ticker="BTC_USD", price=50000.0, timestamp=1234567890),
        Price(ticker="BTC_USD", price=51000.0, timestamp=1234567900)
    ])
    
    use_case = GetAllPricesUseCase(mock_repo)
    result = await use_case.execute("BTC_USD")
    
    assert len(result) == 2
    assert result[0].ticker == "BTC_USD"
    mock_repo.get_all_by_ticker.assert_called_once_with("BTC_USD")


@pytest.mark.asyncio
async def test_get_all_prices_empty():
    # проверяем что пустой список не ломает всё
    mock_repo = MagicMock()
    mock_repo.get_all_by_ticker = AsyncMock(return_value=[])
    
    use_case = GetAllPricesUseCase(mock_repo)
    result = await use_case.execute("ETH_USD")
    
    assert result == []
    assert len(result) == 0


@pytest.mark.asyncio
async def test_get_last_price_ok():
    # обычный кейс - есть цена
    mock_repo = MagicMock()
    expected_price = Price(ticker="BTC_USD", price=50000.0, timestamp=1234567890)
    mock_repo.get_last_by_ticker = AsyncMock(return_value=expected_price)
    
    use_case = GetLastPriceUseCase(mock_repo)
    result = await use_case.execute("BTC_USD")
    
    assert result is not None
    assert result.ticker == "BTC_USD"
    assert result.price == 50000.0


@pytest.mark.asyncio
async def test_get_last_price_not_found():
    # когда цены нет - должен вернуть None
    mock_repo = MagicMock()
    mock_repo.get_last_by_ticker = AsyncMock(return_value=None)
    
    use_case = GetLastPriceUseCase(mock_repo)
    result = await use_case.execute("UNKNOWN")
    
    assert result is None


@pytest.mark.asyncio
async def test_get_price_by_date_found():
    # находим цену по timestamp
    mock_repo = MagicMock()
    expected = Price(ticker="BTC_USD", price=50000.0, timestamp=1234567890)
    mock_repo.get_by_ticker_and_date = AsyncMock(return_value=expected)
    
    use_case = GetPriceByDateUseCase(mock_repo)
    result = await use_case.execute("BTC_USD", 1234567890)
    
    assert result is not None
    assert result.timestamp == 1234567890
    mock_repo.get_by_ticker_and_date.assert_called_once_with("BTC_USD", 1234567890)


@pytest.mark.asyncio
async def test_get_price_by_date_missing():
    # нет цены на эту дату
    mock_repo = MagicMock()
    mock_repo.get_by_ticker_and_date = AsyncMock(return_value=None)
    
    use_case = GetPriceByDateUseCase(mock_repo)
    result = await use_case.execute("BTC_USD", 9999999999)
    
    assert result is None
