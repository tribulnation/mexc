from dataclasses import dataclass as _dataclass
from .time import Time
from .depth import Depth
from .trades import Trades
from .agg_trades import AggTrades
from .avg_price import AvgPrice
from .candles import Candles
from .exchange_info import ExchangeInfo

@_dataclass
class MarketData(
  Time,
  Depth,
  Trades,
  AggTrades,
  AvgPrice,
  Candles,
  ExchangeInfo,
):
  ...