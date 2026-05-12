from datetime import datetime
from typing_extensions import TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class OpenOrder(TypedDict):
  """Open order status."""
  symbol: str
  """Spot symbol."""
  orderId: int | str
  """MEXC order id."""
  orderListId: int
  """Order-list id."""
  clientOrderId: str | None
  """Client order id."""
  price: str
  """Price."""
  origQty: str
  """Original quantity."""
  executedQty: str
  """Executed quantity."""
  cummulativeQuoteQty: str
  """Executed quote quantity."""
  status: str
  """Order status."""
  timeInForce: str | None
  """Time in force."""
  type: str
  """Order type."""
  side: str
  """Order side."""
  stopPrice: str | None
  """Stop price."""
  icebergQty: str | None
  """Iceberg quantity."""
  time: datetime
  """Creation time."""
  updateTime: datetime | None
  """Update time."""
  isWorking: bool
  """Whether active on the order book."""
  origQuoteOrderQty: str
  """Original quote order quantity."""

Response: type[list[OpenOrder] | ErrorResponse] = list[OpenOrder] | ErrorResponse # type: ignore
adapter = validator(Response)

class OpenOrders(AuthSpotMixin):
  async def open_orders(
    self,
    *,
    symbol: str,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> list[OpenOrder]:
    """Returns open orders for a signed account and symbol.

    Args:
      symbol: Spot symbol.
      recv_window: Optional receive window in milliseconds; maximum 60000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#current-open-orders)
    """
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/openOrders', params=params)
    return self.output(r.text, adapter, validate)
