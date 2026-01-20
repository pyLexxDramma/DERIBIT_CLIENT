import time
from typing import Optional

import aiohttp

from src.domain.models import Price


class DeribitClient:
    def __init__(self, base_url: str = "https://www.deribit.com/api/v2"):
        self.base_url = base_url
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def get_index_price(self, index_name: str) -> Optional[float]:
        session = await self._get_session()
        url = f"{self.base_url}/public/get_index_price"
        params = {"index_name": index_name}

        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    result = data.get("result")
                    if result:
                        return result.get("index_price")
                return None
        except Exception:
            return None

    async def get_btc_price(self) -> Optional[Price]:
        price_value = await self.get_index_price("btc_usd")
        if price_value is None:
            return None

        return Price(
            ticker="BTC_USD",
            price=price_value,
            timestamp=int(time.time())
        )

    async def get_eth_price(self) -> Optional[Price]:
        price_value = await self.get_index_price("eth_usd")
        if price_value is None:
            return None

        return Price(
            ticker="ETH_USD",
            price=price_value,
            timestamp=int(time.time())
        )
