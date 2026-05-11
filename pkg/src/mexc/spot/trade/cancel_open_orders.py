from typing_extensions import TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Item."""

Response: type[list[Item] | ErrorResponse] = list[Item] | ErrorResponse # type: ignore
adapter = validator(Response)

class CancelOpenOrders(AuthSpotMixin):
  async def cancel_open_orders(
    self,
    *,
    symbol: str,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> list[Item]:
    """Cancels pending orders for one or more symbols on the signed account.

    Args:
      symbol: One symbol or up to five comma-separated symbols.
      recv_window: Optional receive window in milliseconds; maximum 60000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#cancel-all-open-orders-on-a-symbol"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('DELETE', '/api/v3/openOrders', params=params)
    return self.output(r.text, adapter, validate)
