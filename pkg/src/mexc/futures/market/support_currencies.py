from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import FuturesMixin
from mexc.core import validator

class Response200(TypedDict):
  """Transferable currencies envelope"""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: list[str]
  """Supported transfer currency codes."""

adapter = validator(Response200)

class SupportCurrencies(FuturesMixin):
  async def support_currencies(self, *, validate: bool | None = None) -> Response200:
    """Return currencies supported for futures transfers.

    Args:
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-the-transferable-currencies"""
    params = {}
    r = await self.request('GET', '/api/v1/contract/support_currencies')
    return self.envelope_output(r.text, adapter, validate)
