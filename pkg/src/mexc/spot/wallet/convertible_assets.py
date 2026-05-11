from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Convertible asset."""
  convertMx: NotRequired[str | None]
  """Estimated MX amount after fee."""
  convertUsdt: NotRequired[str | None]
  """Estimated USDT amount."""
  balance: NotRequired[str | None]
  """Convertible balance."""
  asset: NotRequired[str | None]
  """Asset."""
  code: NotRequired[str | None]
  """Per-asset code."""
  message: NotRequired[str | None]
  """Per-asset message."""

Response: type[list[Item] | ErrorResponse] = list[Item] | ErrorResponse # type: ignore
adapter = validator(Response)

class ConvertibleAssets(AuthSpotMixin):
  async def convertible_assets(
    self,
    *,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> list[Item]:
    """Returns dust balances and estimated MX/USDT conversion values for assets that can be converted.

    Args:
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#get-assets-that-can-be-converted-into-mx"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/capital/convert/list', params=params)
    return self.output(r.text, adapter, validate)
