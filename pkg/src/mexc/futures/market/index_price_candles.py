from datetime import datetime
from typing_extensions import Literal, NotRequired, TypedDict
from mexc.futures.core import FuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class Data(TypedDict):
  """K-line series, with each array index representing the same candle across fields."""
  time: list[datetime]
  """Candle open times in seconds."""
  open: list[float]
  """Opening prices."""
  close: list[float]
  """Closing prices."""
  high: list[float]
  """Highest prices."""
  low: list[float]
  """Lowest prices."""
  vol: list[float]
  """Contract volumes."""
  amount: NotRequired[list[float]]
  """Quote amounts."""
  realOpen: NotRequired[list[float]]
  """Live API real opening prices."""
  realClose: NotRequired[list[float]]
  """Live API real closing prices."""
  realHigh: NotRequired[list[float]]
  """Live API real highest prices."""
  realLow: NotRequired[list[float]]
  """Live API real lowest prices."""

class Response200(TypedDict):
  """Index-price K-line envelope"""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: Data

adapter = validator(Response200)

class IndexPriceCandles(FuturesMixin):
  async def index_price_candles(
    self,
    symbol: str,
    *,
    interval: Literal['Min1', 'Min5', 'Min15', 'Min30', 'Min60', 'Hour4', 'Hour8', 'Day1', 'Week1', 'Month1'] | None = None,
    start: Timestamp | None = None,
    end: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Return index-price K-line/candlestick series for a symbol and optional time window.

    Args:
      symbol: Contract symbol, for example BTC_USDT.
      interval: K-line interval: Min1, Min5, Min15, Min30, Min60, Hour4, Hour8, Day1, Week1, or Month1.
      start: Start timestamp in seconds.
      end: End timestamp in seconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-k-line-data-of-the-index-price"""
    params = {}
    if interval is not None:
      params['interval'] = interval
    if start is not None:
      params['start'] = ts.dump_s(start)
    if end is not None:
      params['end'] = ts.dump_s(end)
    r = await self.request('GET', '/api/v1/contract/kline/index_price/{symbol}'.replace('{symbol}', str(symbol)), params=params)
    return self.envelope_output(r.text, adapter, validate)
