from typing_extensions import TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class KycStatusResponse(TypedDict):
  """KYC status response."""
  status: str
  """Verification tier: 1 unverified, 2 primary, 3 advanced, 4 institutional."""

Response: type[KycStatusResponse | ErrorResponse] = KycStatusResponse | ErrorResponse # type: ignore
adapter = validator(Response)

class KycStatus(AuthSpotMixin):
  async def kyc_status(
    self,
    *,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> KycStatusResponse:
    """Returns the account KYC verification tier for the signed spot account.

    Args:
      recv_window: Optional receive window in milliseconds; maximum 60000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#query-kyc-status)
    """
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/kyc/status', params=params)
    return self.output(r.text, adapter, validate)
