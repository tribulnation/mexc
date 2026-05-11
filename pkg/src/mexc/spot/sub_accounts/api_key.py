from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Sub-account API key record."""
  note: NotRequired[str | None]
  """API key note."""
  apiKey: NotRequired[str | None]
  """API public key."""
  permissions: NotRequired[str | None]
  """API key permissions."""
  ip: NotRequired[str | None]
  """API key IP allowlist."""
  creatTime: NotRequired[datetime | None]
  """API key creation time as spelled by the upstream docs."""

class Response200(TypedDict):
  """Sub-account API key wrapper."""
  subAccount: NotRequired[list[Item]]
  """API keys for the requested sub-account."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class ApiKey(AuthSpotMixin):
  async def api_key(
    self,
    *,
    sub_account: str,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns API keys configured for a sub-account under the signed master account.

    Args:
      sub_account: Sub-account name whose API keys should be returned.
      recv_window: Optional signed-request validity window in milliseconds.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#query-the-apikey-of-a-sub-account-for-master-account"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if sub_account is not None:
      params['subAccount'] = sub_account
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/sub-account/apiKey', params=params)
    return self.output(r.text, adapter, validate)
