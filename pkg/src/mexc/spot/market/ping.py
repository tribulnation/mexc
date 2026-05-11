from typing_extensions import Any
from mexc.spot.core import ErrorResponse, SpotMixin
from mexc.core import validator

Response: type[dict[str, Any] | ErrorResponse] = dict[str, Any] | ErrorResponse # type: ignore
adapter = validator(Response)

class Ping(SpotMixin):
  async def ping(self, *, validate: bool | None = None) -> dict[str, Any]:
    """Test connectivity to the MEXC spot REST API.

    Args:
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#test-connectivity"""
    params = {}
    r = await self.request('GET', '/api/v3/ping')
    return self.output(r.text, adapter, validate)
