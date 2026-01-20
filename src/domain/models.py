from dataclasses import dataclass
from typing import Literal

Ticker = Literal["BTC_USD", "ETH_USD"]


@dataclass
class Price:
    ticker: str
    price: float
    timestamp: int
