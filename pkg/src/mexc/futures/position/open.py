from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.futures.core import AuthFuturesMixin
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Futures position record."""
  positionId: NotRequired[int | str]
  """Position identifier."""
  symbol: NotRequired[str]
  """Contract symbol."""
  positionType: NotRequired[int]
  """Position side: Item1 long, 2 short."""
  openType: NotRequired[int]
  """Margin mode: Item1 isolated, 2 cross."""
  state: NotRequired[int]
  """Position state: Item1 holding, 2 system holding, 3 closed."""
  holdVol: NotRequired[float]
  """Held contract volume."""
  frozenVol: NotRequired[float]
  """Frozen position volume."""
  closeVol: NotRequired[float]
  """Closed position volume."""
  holdAvgPrice: NotRequired[float]
  """Average holding price."""
  openAvgPrice: NotRequired[float]
  """Average opening price."""
  closeAvgPrice: NotRequired[float]
  """Average closing price."""
  liquidatePrice: NotRequired[float]
  """Liquidation price."""
  oim: NotRequired[float]
  """Original initial margin."""
  im: NotRequired[float]
  """Initial margin."""
  holdFee: NotRequired[float]
  """Holding fee."""
  realised: NotRequired[float]
  """Realized profit and loss."""
  adlLevel: NotRequired[int]
  """Current ADL level when present."""
  leverage: NotRequired[int]
  """Position leverage."""
  createTime: NotRequired[datetime | str]
  """Creation time."""
  updateTime: NotRequired[datetime | str]
  """Last update time."""
  autoAddIm: NotRequired[bool]
  """Whether automatic margin addition is enabled."""

class Response200(TypedDict):
  """Get open futures positions response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: list[Item]
  """Current open futures positions."""

adapter = validator(Response200)

class Open(AuthFuturesMixin):
  async def open(
    self,
    *,
    symbol: str | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Returns current open holding positions for the signed futures account.

    Args:
      symbol: Optional contract symbol; omitted returns all open positions.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-the-user-39-s-current-holding-position"""
    headers = {}
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    r = await self.signed_request('GET', '/api/v1/private/position/open_positions', params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)
