from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Futures order record."""
  orderId: NotRequired[int | str]
  """Order identifier."""
  symbol: NotRequired[str]
  """Contract symbol."""
  positionId: NotRequired[int | str]
  """Related position identifier."""
  price: NotRequired[float]
  """Order or trigger price."""
  vol: NotRequired[float]
  """Order volume."""
  leverage: NotRequired[int]
  """Leverage used by the order."""
  side: NotRequired[int]
  """Order side: Item1 open long, 2 close short, 3 open short, 4 close long."""
  category: NotRequired[int]
  """Order category."""
  orderType: NotRequired[int]
  """Order type."""
  dealAvgPrice: NotRequired[float]
  """Average filled price."""
  dealVol: NotRequired[float]
  """Filled volume."""
  orderMargin: NotRequired[float]
  """Margin reserved for the order."""
  takerFee: NotRequired[float]
  """Taker fee."""
  makerFee: NotRequired[float]
  """Maker fee."""
  profit: NotRequired[float]
  """Realized close profit."""
  feeCurrency: NotRequired[str]
  """Fee currency."""
  openType: NotRequired[int]
  """Margin mode: Item1 isolated, 2 cross."""
  state: NotRequired[int]
  """Order state."""
  externalOid: NotRequired[str]
  """Client-provided external order id."""
  errorCode: NotRequired[int]
  """Order error code."""
  usedMargin: NotRequired[float]
  """Used margin."""
  createTime: NotRequired[datetime | str]
  """Creation time."""
  updateTime: NotRequired[datetime | str]
  """Last update time."""
  stopLossPrice: NotRequired[float]
  """Attached stop-loss price when present."""
  takeProfitPrice: NotRequired[float]
  """Attached take-profit price when present."""

class Response200(TypedDict):
  """Batch query futures orders by id response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: list[Item]
  """Batch order query results."""

adapter = validator(Response200)

class BatchQuery(AuthFuturesMixin):
  async def batch_query(self, *, order_ids: str, validate: bool | None = None) -> Response200:
    """Returns multiple futures orders for a comma-separated list of order ids.

    Args:
      order_ids: Comma-separated order ids; maximum 50 ids.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#query-the-order-in-bulk-based-on-the-order-number"""
    headers = {}
    params = {}
    if order_ids is not None:
      params['order_ids'] = order_ids
    r = await self.signed_request('GET', '/api/v1/private/order/batch_query', params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)
