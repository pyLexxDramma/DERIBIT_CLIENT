import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import time

from src.infrastructure.external.deribit_client import DeribitClient
from src.domain.models import Price


@pytest.mark.asyncio
async def test_get_index_price_success():
    # мокаем aiohttp response
    client = DeribitClient()
    
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={
        "result": {"index_price": 50000.5}
    })
    
    mock_session = MagicMock()
    mock_session.get = MagicMock()
    mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)
    mock_session.closed = False
    mock_session.close = AsyncMock()
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        price = await client.get_index_price("btc_usd")
        assert price == 50000.5
    
    await client.close()


@pytest.mark.asyncio
async def test_get_index_price_bad_response():
    # когда API возвращает не 200
    client = DeribitClient()
    
    mock_response = MagicMock()
    mock_response.status = 500
    
    mock_session = MagicMock()
    mock_session.get = MagicMock()
    mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)
    mock_session.closed = False
    mock_session.close = AsyncMock()
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        price = await client.get_index_price("btc_usd")
        assert price is None
    
    await client.close()


@pytest.mark.asyncio
async def test_get_btc_price():
    # проверяем что get_btc_price правильно формирует Price объект
    client = DeribitClient()
    
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={
        "result": {"index_price": 50000.0}
    })
    
    mock_session = MagicMock()
    mock_session.get = MagicMock()
    mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)
    mock_session.closed = False
    mock_session.close = AsyncMock()
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        with patch('time.time', return_value=1234567890):
            result = await client.get_btc_price()
            
            assert result is not None
            assert isinstance(result, Price)
            assert result.ticker == "BTC_USD"
            assert result.price == 50000.0
            assert result.timestamp == 1234567890
    
    await client.close()


@pytest.mark.asyncio
async def test_get_btc_price_none():
    # если API не вернул цену
    client = DeribitClient()
    
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={"result": None})
    
    mock_session = MagicMock()
    mock_session.get = MagicMock()
    mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)
    mock_session.closed = False
    mock_session.close = AsyncMock()
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        result = await client.get_btc_price()
        assert result is None
    
    await client.close()


@pytest.mark.asyncio
async def test_get_eth_price():
    # аналогично для ETH
    client = DeribitClient()
    
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={
        "result": {"index_price": 3000.5}
    })
    
    mock_session = MagicMock()
    mock_session.get = MagicMock()
    mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)
    mock_session.closed = False
    mock_session.close = AsyncMock()
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        with patch('time.time', return_value=1234567890):
            result = await client.get_eth_price()
            
            assert result.ticker == "ETH_USD"
            assert result.price == 3000.5
    
    await client.close()
