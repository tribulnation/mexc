from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import validator

class Body(TypedDict):
  """Cancel futures order by external id request body."""
  symbol: str
  """Contract symbol."""
  externalOid: str
  """External order identifier."""

class Response200(TypedDict):
  """Futures write endpoint response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""

adapter = validator(Response200)

class CancelExternalOrder(AuthFuturesMixin):
  async def cancel_external_order(
    self,
    body: Body,
    *,
    validate: bool | None = None
  ) -> Response200:
    """Cancels one uncompleted order under a contract by client-supplied external order id.

    Args:
      body: Request body.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#cancel-the-order-according-to-the-external-order-id-under-maintenance"""
    params = {}
    r = await self.signed_post('/api/v1/private/order/cancel_with_external', json=body)
    return self.envelope_output(r.text, adapter, validate)
