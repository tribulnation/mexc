from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Response200(TypedDict):
  """Withdrawal cancellation response."""
  id: NotRequired[str | None]
  """Canceled withdrawal id."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class CancelWithdraw(AuthSpotMixin):
  async def cancel_withdraw(
    self,
    *,
    id: str,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Cancels a pending withdrawal by withdrawal id.

    Args:
      id: Withdrawal id to cancel.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#cancel-withdraw"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if id is not None:
      params['id'] = id
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('DELETE', '/api/v3/capital/withdraw', params=params)
    return self.output(r.text, adapter, validate)
