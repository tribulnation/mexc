from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Data(TypedDict):
  """Response data."""
  mxDeductEnable: NotRequired[bool]
  """Whether MX deduction is enabled."""

class Response200(TypedDict):
  """Wrapper response."""
  data: NotRequired[Data]
  code: NotRequired[int]
  """Response code."""
  msg: NotRequired[str]
  """Response message."""
  timestamp: NotRequired[datetime]
  """Response timestamp."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class MxDeductStatus(AuthSpotMixin):
  async def mx_deduct_status(
    self,
    *,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns whether MX deduction for spot commission fees is enabled.

    Args:
      recv_window: Optional receive window in milliseconds; maximum 60000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#query-mx-deduct-status"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/mxDeduct/enable', params=params)
    return self.output(r.text, adapter, validate)
