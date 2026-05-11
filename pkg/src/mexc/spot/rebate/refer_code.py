from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Response200(TypedDict):
  """Referral code response."""
  referCode: NotRequired[str]
  """Referral code for the signed account."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class ReferCode(AuthSpotMixin):
  async def refer_code(
    self,
    *,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns the referral code associated with the signed account.

    Args:
      recv_window: Optional receive window in milliseconds.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#query-refercode"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/rebate/referCode', params=params)
    return self.output(r.text, adapter, validate)
