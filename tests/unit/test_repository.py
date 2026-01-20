import pytest
from unittest.mock import AsyncMock, MagicMock

from src.infrastructure.database.repositories.price_repository import PriceRepository
from src.domain.models import Price


@pytest.mark.asyncio
async def test_get_all_by_ticker():
    # мокаем connection pool и результат запроса
    mock_db = MagicMock()
    mock_pool = AsyncMock()
    mock_conn = AsyncMock()
    
    mock_rows = [
        {"ticker": "BTC_USD", "price": 50000.0, "timestamp": 1234567890},
        {"ticker": "BTC_USD", "price": 51000.0, "timestamp": 1234567900}
    ]
    mock_conn.fetch = AsyncMock(return_value=mock_rows)
    mock_conn.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_conn.__aexit__ = AsyncMock(return_value=None)
    
    mock_pool.acquire = MagicMock(return_value=mock_conn)
    mock_db.get_pool = AsyncMock(return_value=mock_pool)
    
    repo = PriceRepository(mock_db)
    result = await repo.get_all_by_ticker("BTC_USD")
    
    assert len(result) == 2
    assert all(isinstance(p, Price) for p in result)
    assert result[0].ticker == "BTC_USD"


@pytest.mark.asyncio
async def test_get_last_by_ticker():
    # проверяем что последняя цена возвращается
    mock_db = MagicMock()
    mock_pool = AsyncMock()
    mock_conn = AsyncMock()
    
    mock_row = {"ticker": "BTC_USD", "price": 50000.0, "timestamp": 1234567890}
    mock_conn.fetchrow = AsyncMock(return_value=mock_row)
    mock_conn.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_conn.__aexit__ = AsyncMock(return_value=None)
    
    mock_pool.acquire = MagicMock(return_value=mock_conn)
    mock_db.get_pool = AsyncMock(return_value=mock_pool)
    
    repo = PriceRepository(mock_db)
    result = await repo.get_last_by_ticker("BTC_USD")
    
    assert result is not None
    assert result.price == 50000.0


@pytest.mark.asyncio
async def test_get_last_by_ticker_none():
    # когда нет записей
    mock_db = MagicMock()
    mock_pool = AsyncMock()
    mock_conn = AsyncMock()
    
    mock_conn.fetchrow = AsyncMock(return_value=None)
    mock_conn.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_conn.__aexit__ = AsyncMock(return_value=None)
    
    mock_pool.acquire = MagicMock(return_value=mock_conn)
    mock_db.get_pool = AsyncMock(return_value=mock_pool)
    
    repo = PriceRepository(mock_db)
    result = await repo.get_last_by_ticker("UNKNOWN")
    
    assert result is None


@pytest.mark.asyncio
async def test_get_by_ticker_and_date():
    # поиск по тикеру и timestamp
    mock_db = MagicMock()
    mock_pool = AsyncMock()
    mock_conn = AsyncMock()
    
    mock_row = {"ticker": "BTC_USD", "price": 50000.0, "timestamp": 1234567890}
    mock_conn.fetchrow = AsyncMock(return_value=mock_row)
    mock_conn.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_conn.__aexit__ = AsyncMock(return_value=None)
    
    mock_pool.acquire = MagicMock(return_value=mock_conn)
    mock_db.get_pool = AsyncMock(return_value=mock_pool)
    
    repo = PriceRepository(mock_db)
    result = await repo.get_by_ticker_and_date("BTC_USD", 1234567890)
    
    assert result is not None
    assert result.timestamp == 1234567890


@pytest.mark.asyncio
async def test_save():
    # проверяем что save вызывает execute с правильными параметрами
    mock_db = MagicMock()
    mock_pool = AsyncMock()
    mock_conn = AsyncMock()
    
    mock_conn.execute = AsyncMock()
    mock_conn.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_conn.__aexit__ = AsyncMock(return_value=None)
    
    mock_pool.acquire = MagicMock(return_value=mock_conn)
    mock_db.get_pool = AsyncMock(return_value=mock_pool)
    
    repo = PriceRepository(mock_db)
    price = Price(ticker="BTC_USD", price=50000.0, timestamp=1234567890)
    
    await repo.save(price)
    
    # проверяем что execute был вызван
    mock_conn.execute.assert_called_once()
    call_args = mock_conn.execute.call_args
    assert "INSERT INTO prices" in call_args[0][0]
