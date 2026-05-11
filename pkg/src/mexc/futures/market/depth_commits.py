from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import FuturesMixin
from mexc.core import validator

class Item(TypedDict):
  """Depth snapshot or incremental depth commit."""
  asks: list[list[float]]
  """Ask-side depth levels."""
  bids: list[list[float]]
  """Bid-side depth levels."""
  version: int
  """Depth version number."""
  timestamp: NotRequired[datetime]
  """System timestamp in milliseconds."""

class Response200(TypedDict):
  """Depth commits envelope"""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: list[Item]
  """Latest depth commit records."""

adapter = validator(Response200)

class DepthCommits(FuturesMixin):
  async def depth_commits(
    self,
    symbol: str,
    limit: int,
    *,
    validate: bool | None = None
  ) -> Response200:
    """Return the latest N depth snapshots/commits for a contract.

    Args:
      symbol: Contract symbol, for example BTC_USDT.
      limit: Number of latest depth commits to return.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-a-snapshot-of-the-latest-n-depth-information-of-the-contract"""
    params = {}
    r = await self.request('GET', '/api/v1/contract/depth_commits/{symbol}/{limit}'.replace('{symbol}', str(symbol)).replace('{limit}', str(limit)))
    return self.envelope_output(r.text, adapter, validate)
