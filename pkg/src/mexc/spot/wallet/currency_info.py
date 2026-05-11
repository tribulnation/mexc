from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class NetworkListItem(TypedDict):
  """Network settings."""
  coin: NotRequired[str | None]
  """Currency code."""
  depositEnable: NotRequired[bool | None]
  """Whether deposits are enabled on this network."""
  withdrawEnable: NotRequired[bool | None]
  """Whether withdrawals are enabled on this network."""
  withdrawFee: NotRequired[str | None]
  """Withdrawal fee."""
  withdrawMax: NotRequired[str | None]
  """Maximum withdrawal amount."""
  withdrawMin: NotRequired[str | None]
  """Minimum withdrawal amount."""
  contract: NotRequired[str | None]
  """Token contract address, when applicable."""
  network: NotRequired[str | None]
  """Withdrawal network identifier."""
  netWork: NotRequired[str | None]
  """New withdrawal network identifier used by newer withdraw endpoint."""
  memo: NotRequired[str | None]
  """Memo/tag requirement, when present."""

class Response200Item(TypedDict):
  """Currency configuration."""
  coin: NotRequired[str | None]
  """Currency code."""
  Name: NotRequired[str | None]
  """Currency display name."""
  networkList: NotRequired[list[NetworkListItem]]
  """Network-specific deposit and withdrawal settings."""

Response: type[list[Response200Item] | ErrorResponse] = list[Response200Item] | ErrorResponse # type: ignore
adapter = validator(Response)

class CurrencyInfo(AuthSpotMixin):
  async def currency_info(
    self,
    *,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> list[Response200Item]:
    """Returns supported currencies, deposit/withdrawal availability, network limits, fees, and contract metadata for wallet operations.

    Args:
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#query-the-currency-information"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/capital/config/getall', params=params)
    return self.output(r.text, adapter, validate)
