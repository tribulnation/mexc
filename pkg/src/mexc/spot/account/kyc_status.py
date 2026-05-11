from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Response200(TypedDict):
  """KYC status response."""
  status: NotRequired[str]
  """Verification tier: Item1 unverified, 2 primary, 3 advanced, 4 institutional."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class KycStatus(AuthSpotMixin):
  async def kyc_status(
    self,
    *,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns the account KYC verification tier for the signed spot account.

    Args:
      recv_window: Optional receive window in milliseconds; maximum 60000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#query-kyc-status"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/kyc/status', params=params)
    return self.output(r.text, adapter, validate)
