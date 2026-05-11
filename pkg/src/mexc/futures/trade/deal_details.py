from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Futures deal record."""
  id: NotRequired[int | str]
  """Trade/deal identifier."""
  symbol: NotRequired[str]
  """Contract symbol."""
  side: NotRequired[int]
  """Order side."""
  vol: NotRequired[float]
  """Executed volume."""
  price: NotRequired[float]
  """Execution price."""
  feeCurrency: NotRequired[str]
  """Fee currency."""
  fee: NotRequired[float]
  """Charged fee."""
  timestamp: NotRequired[datetime | str]
  """Execution timestamp."""
  profit: NotRequired[float]
  """Realized profit."""
  isTaker: NotRequired[bool]
  """Whether the fill was taker-side."""
  taker: NotRequired[bool]
  """Whether the fill was taker-side; name used by some examples."""
  category: NotRequired[int]
  """Order category."""
  orderId: NotRequired[int | str]
  """Related order identifier."""

class Response200(TypedDict):
  """Get futures order deal details response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: list[Item]
  """Order deal details."""

adapter = validator(Response200)

class DealDetails(AuthFuturesMixin):
  async def deal_details(self, order_id: str, *, validate: bool | None = None) -> Response200:
    """Returns fills/deals for a futures order id.

    Args:
      order_id: Exchange order id.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-order-transaction-details-based-on-the-order-id"""
    headers = {}
    params = {}
    r = await self.signed_request('GET', '/api/v1/private/order/deal_details/{order_id}'.replace('{order_id}', str(order_id)), params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)
