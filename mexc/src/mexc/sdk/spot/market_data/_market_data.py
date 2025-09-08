from dataclasses import dataclass
from .depth import Depth
from .exchange_info import ExchangeInfo
from .candles import Candles

@dataclass
class MarketData(Depth, ExchangeInfo, Candles):
  ...