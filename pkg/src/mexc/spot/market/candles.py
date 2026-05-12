from datetime import datetime
from typing_extensions import Literal
from mexc.spot.core import ErrorResponse, SpotMixin
from mexc.core import Timestamp, timestamp as ts, validator

SpotCandle = tuple[datetime, str, str, str, str, str, datetime, str]

Response: type[list[SpotCandle] | ErrorResponse] = list[SpotCandle] | ErrorResponse # type: ignore
adapter = validator(Response)

class Candles(SpotMixin):
  async def candles(
    self,
    *,
    symbol: str,
    interval: Literal['1m', '5m', '15m', '30m', '60m', '4h', '1d', '1W', '1M'],
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    limit: int | None = None,
    validate: bool | None = None
  ) -> list[SpotCandle]:
    """Return spot kline/candlestick rows for a symbol.

    Args:
      symbol: Spot symbol.
      interval: Kline interval.
      start_time: Start timestamp in milliseconds.
      end_time: End timestamp in milliseconds.
      limit: Maximum number of candles.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#kline-candlestick-data)
    """
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if interval is not None:
      params['interval'] = interval
    if start_time is not None:
      params['startTime'] = ts.dump_ms(start_time)
    if end_time is not None:
      params['endTime'] = ts.dump_ms(end_time)
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', '/api/v3/klines', params=params)
    return self.output(r.text, adapter, validate)
