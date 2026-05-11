from datetime import datetime
from typing_extensions import AsyncIterator, NotRequired, TypedDict
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
  """Get historical futures positions response envelope."""
  success: bool
  """Whether the API request succeeded."""
  code: NotRequired[int]
  """MEXC response code; zero indicates success when present."""
  message: NotRequired[str]
  """Error or status message when present."""
  data: list[Item]
  """Historical futures positions."""

adapter = validator(Response200)

class History(AuthFuturesMixin):
  async def history(
    self,
    *,
    symbol: str | None = None,
    type_: int | None = None,
    page_num: int,
    page_size: int,
    validate: bool | None = None
  ) -> Response200:
    """Returns paginated historical position records for the signed futures account.

    Args:
      symbol: Contract symbol filter.
      type_: Position type filter: 1 long, 2 short.
      page_num: Page number; default is 1.
      page_size: Page size; default 20, maximum 100.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/contract_v1_en/#get-the-user-s-history-position-information"""
    headers = {}
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    if type_ is not None:
      params['type'] = type_
    if page_num is not None:
      params['page_num'] = page_num
    if page_size is not None:
      params['page_size'] = page_size
    r = await self.signed_request('GET', '/api/v1/private/position/list/history_positions', params=params or None, headers=headers)
    return self.envelope_output(r.text, adapter, validate)

  async def history_paged(self, *, symbol: str | None = None, type_: int | None = None, page_size: int, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[Response200]:
    """Yield pages from `history` until the response reports the final page."""
    page = 1
    while True:
      response = await self.history(symbol=symbol, type_=type_, page_size=page_size, page_num=page, validate=validate)
      yield response
      if max_pages is not None and page >= max_pages:
        break
      data = response.get('data') if isinstance(response, dict) else None
      total = None
      if isinstance(data, dict):
        total = data.get('totalPage') or data.get('totalPageNum')
      if total is None and isinstance(response, dict):
        total = response.get('totalPage') or response.get('totalPageNum')
      if total is None:
        if data == [] or response == []:
          break
        if max_pages is None:
          break
        page += 1
        continue
      if total is None or page >= total:
        break
      page += 1
