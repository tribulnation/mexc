from .agg_trades import AggTrades
from .avg_price import AvgPrice
from .book_ticker import BookTicker
from .candles import Candles
from .default_symbols import DefaultSymbols
from .depth import Depth
from .etf_info import EtfInfo
from .exchange_info import ExchangeInfo
from .historical_trades import HistoricalTrades
from .ping import Ping
from .ticker_24hr import Ticker24hr
from .ticker_price import TickerPrice
from .time import Time
from .trades import Trades

class Market(AggTrades, AvgPrice, BookTicker, Candles, DefaultSymbols, Depth, EtfInfo, ExchangeInfo, HistoricalTrades, Ping, Ticker24hr, TickerPrice, Time, Trades):
  ...
