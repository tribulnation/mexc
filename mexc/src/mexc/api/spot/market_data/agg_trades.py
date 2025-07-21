from typing_extensions import TypedDict, overload
from datetime import datetime
from pydantic import RootModel
from mexc.core import ClientMixin, timestamp as ts, ApiError

class AggTrade(TypedDict):
  """Aggregate tradeId"""
  a: str | None
  """First tradeId"""
  f: str | None
  """Last tradeId"""
  l: str | None
  """Price"""
  p: str
  """Quantity"""
  q: str
  """Timestamp"""
  T: int
  """Is buyer maker"""
  m: bool
  """Is best match"""
  M: bool


class Response(RootModel):
  root: list[AggTrade] | ApiError

class AggTrades(ClientMixin):
  @overload
  async def agg_trades(
    self, symbol: str, *, limit: int | None = None,
    validate: bool = True,
  ) -> ApiError | list[AggTrade]:
    ...
  @overload
  async def agg_trades(
    self, symbol: str, *, limit: int | None = None,
    start: datetime, end: datetime,
    validate: bool = True,
  ) -> ApiError | list[AggTrade]:
    ...
  async def agg_trades(
    self, symbol: str, *, limit: int | None = None,
    start: datetime | None = None, end: datetime | None = None,
    validate: bool = True,
  ) -> ApiError | list[AggTrade]:
    """Get aggregate trades for a given symbol.
    
    - `symbol`: The symbol being traded, e.g. `BTCUSDT`.
    - `limit`: The maximum number of trades to return (default: 500, max: 1000).
    - `start`: The start time to query. If given, only trades after this time will be returned.
    - `end`: The end time to query. If given, only trades before this time will be returned.
    - `validate`: Whether to validate the response against the expected schema (default: True).

    > [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#compressed-aggregate-trades-list)
    """
    params: dict = {'symbol': symbol}
    if limit is not None:
      params['limit'] = limit
    if start is not None:
      params['startTime'] = ts.dump(start)
    if end is not None:
      params['endTime'] = ts.dump(end)
    r = await self.request('GET', '/api/v3/aggTrades', params=params)
    return Response.model_validate_json(r.text).root if validate else r.json()