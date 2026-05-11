from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Balance."""
  asset: NotRequired[str]
  free: NotRequired[str]
  locked: NotRequired[str]

class Response200(TypedDict):
  """Account information response."""
  canTrade: NotRequired[bool]
  """Whether spot trading is enabled."""
  canWithdraw: NotRequired[bool]
  """Whether withdrawals are enabled."""
  canDeposit: NotRequired[bool]
  """Whether deposits are enabled."""
  updateTime: NotRequired[datetime | None]
  """Account update time."""
  accountType: NotRequired[str]
  """Account type."""
  balances: NotRequired[list[Item]]
  """Asset balances."""
  permissions: NotRequired[list[str]]
  """Account permissions."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class Info(AuthSpotMixin):
  async def info(
    self,
    *,
    recv_window: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns trading permissions and spot balances for the signed account.

    Args:
      recv_window: Optional receive window in milliseconds; maximum 60000.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#account-information"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if recv_window is not None:
      params['recvWindow'] = recv_window
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/account', params=params)
    return self.output(r.text, adapter, validate)
