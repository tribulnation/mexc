from typing_extensions import TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Item."""

Response: type[list[Item] | ErrorResponse] = list[Item] | ErrorResponse # type: ignore
adapter = validator(Response)

class Trades(AuthSpotMixin):
  async def trades(
    self,
    *,
    symbol: str,
    order_id: str | None = None,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    limit: int | None = None,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> list[Item]:
    """Returns account trade executions for a symbol, limited to recent history.

    Args:
      symbol: Spot symbol.
      order_id: Order id filter.
      start_time: Window start time.
      end_time: Window end time.
      limit: Default 100; maximum 100.
      recv_window: Optional receive window in milliseconds; maximum 60000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#account-trade-list"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if order_id is not None:
      params['orderId'] = order_id
    if start_time is not None:
      params['startTime'] = ts.dump_ms(start_time)
    if end_time is not None:
      params['endTime'] = ts.dump_ms(end_time)
    if limit is not None:
      params['limit'] = limit
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/myTrades', params=params)
    return self.output(r.text, adapter, validate)
