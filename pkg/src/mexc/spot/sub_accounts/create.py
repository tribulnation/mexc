from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Body(TypedDict):
  subAccount: NotRequired[str]
  """Name to assign to the new sub-account."""
  note: NotRequired[str]
  """Operator note stored with the sub-account."""

class Response200(TypedDict):
  """Created sub-account record."""
  subAccount: NotRequired[str | None]
  """Created sub-account name."""
  note: NotRequired[str | None]
  """Sub-account note."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class Create(AuthSpotMixin):
  async def create(
    self,
    *,
    sub_account: str,
    note: str,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Creates a new sub-account under the signed master account.

    Args:
      sub_account: Name to assign to the new sub-account.
      note: Operator note stored with the sub-account.
      recv_window: Optional signed-request validity window in milliseconds.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#create-a-sub-account-for-master-account"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if sub_account is not None:
      params['subAccount'] = sub_account
    if note is not None:
      params['note'] = note
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('POST', '/api/v3/sub-account/virtualSubAccount', params=params)
    return self.output(r.text, adapter, validate)
