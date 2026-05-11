from typing_extensions import Any, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Item."""

Response: type[list[Item] | ErrorResponse] = list[Item] | ErrorResponse # type: ignore
adapter = validator(Response)

class BatchOrders(AuthSpotMixin):
  async def batch_orders(
    self,
    *,
    batch_orders: list[dict[str, Any]],
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> list[Item]:
    """Creates up to 20 orders for the same symbol in one signed request.

    Args:
      batch_orders: List of order objects; maximum 20 orders with the same symbol.
      recv_window: Optional receive window in milliseconds; maximum 60000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#batch-orders"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if batch_orders is not None:
      params['batchOrders'] = batch_orders
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('POST', '/api/v3/batchOrders', params=params)
    return self.output(r.text, adapter, validate)
