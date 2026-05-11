from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Body(TypedDict):
  subAccount: NotRequired[str]
  """Sub-account name for which to create the API key."""
  note: NotRequired[str]
  """API key note."""
  permissions: NotRequired[str]
  """Comma-separated API key permissions."""
  ip: NotRequired[str]
  """Optional comma-separated IP allowlist."""

class Response200(TypedDict):
  """Created sub-account API key."""
  subAccount: NotRequired[str | None]
  """Sub-account name."""
  note: NotRequired[str | None]
  """API key note."""
  apiKey: NotRequired[str | None]
  """API public key."""
  secretKey: NotRequired[str | None]
  """API secret key returned at creation time."""
  permissions: NotRequired[str | None]
  """API key permissions."""
  ip: NotRequired[str | None]
  """API key IP allowlist."""
  creatTime: NotRequired[datetime | None]
  """API key creation time as spelled by the upstream docs."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class CreateApiKey(AuthSpotMixin):
  async def create_api_key(
    self,
    *,
    sub_account: str,
    note: str,
    permissions: str,
    ip: str | None = None,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Creates an API key for a sub-account under the signed master account.

    Args:
      sub_account: Sub-account name for which to create the API key.
      note: API key note.
      permissions: Comma-separated API key permissions, such as SPOT_ACCOUNT_READ or SPOT_DEAL_WRITE.
      ip: Optional comma-separated IP allowlist. The official docs allow up to 20 addresses.
      recv_window: Optional signed-request validity window in milliseconds.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#create-an-apikey-for-a-sub-account-for-master-account"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if sub_account is not None:
      params['subAccount'] = sub_account
    if note is not None:
      params['note'] = note
    if permissions is not None:
      params['permissions'] = permissions
    if ip is not None:
      params['ip'] = ip
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('POST', '/api/v3/sub-account/apiKey', params=params)
    return self.output(r.text, adapter, validate)
