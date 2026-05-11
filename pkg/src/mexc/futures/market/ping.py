from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import FuturesMixin
from mexc.core import validator

class Response200(TypedDict):
  """Server time envelope"""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: datetime
  """Server timestamp in milliseconds."""

adapter = validator(Response200)

class Ping(FuturesMixin):
  async def ping(self, *, validate: bool | None = None) -> Response200:
    """Return the current MEXC futures server time.

    Args:
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-the-server-time"""
    params = {}
    r = await self.request('GET', '/api/v1/contract/ping')
    return self.envelope_output(r.text, adapter, validate)
