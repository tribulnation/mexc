from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class DealDetailsItem(TypedDict):
  """Futures deal record."""
  id: int | str
  """Trade/deal identifier."""
  symbol: str
  """Contract symbol."""
  side: int
  """Order side."""
  vol: float
  """Executed volume."""
  price: float
  """Execution price."""
  feeCurrency: str
  """Fee currency."""
  fee: float
  """Charged fee."""
  timestamp: datetime | str
  """Execution timestamp."""
  profit: float
  """Realized profit."""
  isTaker: NotRequired[bool]
  """Whether the fill was taker-side."""
  taker: bool
  """Whether the fill was taker-side; name used by some examples."""
  category: int
  """Order category."""
  orderId: int | str
  """Related order identifier."""

class DealDetailsResponse(TypedDict):
  """Get futures order deal details response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: NotRequired[list[DealDetailsItem]]
  """Order deal details."""

adapter = validator(DealDetailsResponse)

class DealDetails(AuthFuturesMixin):
  async def deal_details(
    self,
    order_id: str,
    *,
    validate: bool | None = None
  ) -> DealDetailsResponse:
    """Returns fills/deals for a futures order id.

    Args:
      order_id: Exchange order id.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-order-transaction-details-based-on-the-order-id)
    """
    headers = {}
    params = {}
    r = await self.signed_request('GET', '/api/v1/private/order/deal_details/{order_id}'.replace('{order_id}', str(order_id)), params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)
