from datetime import datetime
from typing_extensions import TypedDict
from mexc.spot.core import ErrorResponse, SpotMixin
from mexc.core import Timestamp, timestamp as ts, validator

class AggTradesItem(TypedDict):
  a: int | str | None
  """Aggregate trade id; can be null."""
  f: int | str | None
  """First trade id; can be null."""
  l: int | str | None
  """Last trade id; can be null."""
  p: str
  """Price."""
  q: str
  """Quantity."""
  T: datetime
  """Trade timestamp in milliseconds."""
  m: bool
  """Whether buyer was maker."""
  M: bool
  """Whether this was the best match."""

Response: type[list[AggTradesItem] | ErrorResponse] = list[AggTradesItem] | ErrorResponse # type: ignore
adapter = validator(Response)

class AggTrades(SpotMixin):
  async def agg_trades(
    self,
    *,
    symbol: str,
    limit: int | None = None,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    validate: bool | None = None
  ) -> list[AggTradesItem]:
    """Return aggregate public trades for a spot symbol.

    Args:
      symbol: Spot symbol.
      limit: Maximum number of aggregate trades.
      start_time: Start timestamp in milliseconds.
      end_time: End timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#compressed-aggregate-trades-list)
    """
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if limit is not None:
      params['limit'] = limit
    if start_time is not None:
      params['startTime'] = ts.dump_ms(start_time)
    if end_time is not None:
      params['endTime'] = ts.dump_ms(end_time)
    r = await self.request('GET', '/api/v3/aggTrades', params=params)
    return self.output(r.text, adapter, validate)
