from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import validator

class Item(TypedDict):
  """Per-order cancel result."""
  orderId: NotRequired[int | str]
  """Order identifier."""
  errorCode: NotRequired[int]
  """Cancel result code; zero indicates success."""
  errorMsg: NotRequired[str]
  """Cancel result message."""

class Response200(TypedDict):
  """Futures cancel response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: NotRequired[list[Item]]
  """Per-order cancel results."""

adapter = validator(Response200)

class CancelOrder(AuthFuturesMixin):
  async def cancel_order(
    self,
    listint_str: list[int | str],
    *,
    validate: bool | None = None
  ) -> Response200:
    """Cancels up to 50 pending futures orders by order id.

    Args:
      listint_str: Request parameter.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#cancel-the-order-under-maintenance"""
    params = {}
    r = await self.signed_post('/api/v1/private/order/cancel', json=listint_str)
    return self.envelope_output(r.text, adapter, validate)
