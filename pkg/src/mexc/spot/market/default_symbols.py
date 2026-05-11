from typing_extensions import Any, NotRequired, TypedDict
from mexc.spot.core import ErrorResponse, SpotMixin
from mexc.core import validator

class Response200(TypedDict):
  code: NotRequired[int]
  """API status code."""
  data: list[str]
  """Default spot symbols."""
  msg: NotRequired[Any]
  """API message, often null."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class DefaultSymbols(SpotMixin):
  async def default_symbols(self, *, validate: bool | None = None) -> Response200:
    """Return MEXC spot default symbols.

    Args:
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#api-default-symbol"""
    params = {}
    r = await self.request('GET', '/api/v3/defaultSymbols')
    return self.output(r.text, adapter, validate)
