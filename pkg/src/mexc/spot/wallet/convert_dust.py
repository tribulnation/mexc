from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Failed conversion."""
  asset: NotRequired[str | None]
  """Asset."""
  message: NotRequired[str | None]
  """Failure message."""
  code: NotRequired[str | None]
  """Failure code."""

class Response200(TypedDict):
  """Dust conversion response."""
  successList: NotRequired[list[str]]
  """Successfully converted assets."""
  failedList: NotRequired[list[Item]]
  """Failed conversion entries."""
  totalConvert: NotRequired[str | None]
  """Total converted MX amount after fee."""
  convertFee: NotRequired[str | None]
  """Conversion fee."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class ConvertDust(AuthSpotMixin):
  async def convert_dust(
    self,
    *,
    asset: str,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Converts small asset balances into MX.

    Args:
      asset: Comma-separated assets to convert; max 15 assets.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#dust-transfer"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if asset is not None:
      params['asset'] = asset
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('POST', '/api/v3/capital/convert', params=params)
    return self.output(r.text, adapter, validate)
