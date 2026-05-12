from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class OrderData(TypedDict):
  """Futures order record."""
  orderId: int | str
  """Order identifier."""
  symbol: str
  """Contract symbol."""
  positionId: int | str
  """Related position identifier."""
  price: float
  """Order or trigger price."""
  vol: float
  """Order volume."""
  leverage: int
  """Leverage used by the order."""
  side: int
  """Order side: 1 open long, 2 close short, 3 open short, 4 close long."""
  category: int
  """Order category."""
  orderType: int
  """Order type."""
  dealAvgPrice: float
  """Average filled price."""
  dealVol: float
  """Filled volume."""
  orderMargin: float
  """Margin reserved for the order."""
  takerFee: float
  """Taker fee."""
  makerFee: float
  """Maker fee."""
  profit: float
  """Realized close profit."""
  feeCurrency: str
  """Fee currency."""
  openType: int
  """Margin mode: 1 isolated, 2 cross."""
  state: int
  """Order state."""
  externalOid: str
  """Client-provided external order id."""
  errorCode: int
  """Order error code."""
  usedMargin: float
  """Used margin."""
  createTime: datetime | str
  """Creation time."""
  updateTime: datetime | str
  """Last update time."""
  stopLossPrice: NotRequired[float]
  """Attached stop-loss price when present."""
  takeProfitPrice: NotRequired[float]
  """Attached take-profit price when present."""

class OrderResponse(TypedDict):
  """Get futures order by id response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: NotRequired[OrderData]

adapter = validator(OrderResponse)

class Order(AuthFuturesMixin):
  async def order(self, order_id: str, *, validate: bool | None = None) -> OrderResponse:
    """Returns a futures order by exchange order id.

    Args:
      order_id: Exchange order id.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/contract_v1_en/#query-the-order-based-on-the-order-number)
    """
    headers = {}
    params = {}
    r = await self.signed_request('GET', '/api/v1/private/order/get/{order_id}'.replace('{order_id}', str(order_id)), params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)
