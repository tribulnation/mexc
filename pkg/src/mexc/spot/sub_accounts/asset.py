from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Single asset balance."""
  asset: NotRequired[str | None]
  """Asset symbol."""
  free: NotRequired[str | None]
  """Available balance."""
  locked: NotRequired[str | None]
  """Locked balance."""

class Response200(TypedDict):
  """Sub-account balances wrapper."""
  balances: NotRequired[list[Item]]
  """Asset balances for the sub-account."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class Asset(AuthSpotMixin):
  async def asset(
    self,
    *,
    sub_account: str,
    account_type: str,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns balances for a single sub-account.

    Args:
      sub_account: Sub-account name to query. The official docs only support one sub-account per request.
      account_type: Account type to query. The docs list SPOT and FUTURES but say only SPOT is currently supported.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#query-sub-account-asset"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if sub_account is not None:
      params['subAccount'] = sub_account
    if account_type is not None:
      params['accountType'] = account_type
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/sub-account/asset', params=params)
    return self.output(r.text, adapter, validate)
