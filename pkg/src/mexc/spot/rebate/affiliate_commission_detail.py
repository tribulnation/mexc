from typing_extensions import AsyncIterator, NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Affiliate record."""
  type: NotRequired[int]
  """Commission type: Item1 spot, 2 futures, 3 ETF."""
  sourceType: NotRequired[int]
  """Source type: Item1 referral, 2 sub-affiliate."""
  state: NotRequired[int]
  """Commission state."""
  date: NotRequired[int]
  """Trade date."""
  uid: NotRequired[str]
  """User id."""
  rate: NotRequired[float | str]
  """Commission rate."""
  symbol: NotRequired[str]
  """Trading symbol."""
  takerAmount: NotRequired[str]
  """Taker trade amount."""
  makerAmount: NotRequired[str]
  """Maker trade amount."""
  amountCurrency: NotRequired[str]
  """Trade amount currency."""
  usdtAmount: NotRequired[str]
  """USDT trade amount."""
  commission: NotRequired[str]
  """Commission amount."""
  currency: NotRequired[str]
  """Commission currency."""

class Data(TypedDict):
  """Paginated affiliate data."""
  pageSize: NotRequired[int]
  """Number of records requested per page."""
  totalCount: NotRequired[int]
  """Total number of matching records."""
  totalPage: NotRequired[int]
  """Total number of result pages."""
  currentPage: NotRequired[int]
  """Current result page."""
  resultList: NotRequired[list[Item]]
  """Affiliate records for the page."""
  totalCommissionUsdtAmount: NotRequired[str]
  """Total commission in USDT."""
  totalTradeUsdtAmount: NotRequired[str]
  """Total trade volume in USDT."""

class Response200(TypedDict):
  """Affiliate wrapper response."""
  success: NotRequired[bool]
  """Whether the request succeeded."""
  code: NotRequired[int]
  """Business response code."""
  message: NotRequired[str | None]
  """Business response message."""
  data: NotRequired[Data]

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class AffiliateCommissionDetail(AuthSpotMixin):
  async def affiliate_commission_detail(
    self,
    *,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    invite_code: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
    type_: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Affiliate-only endpoint returning detailed commission records by type, source, date, user, and asset.

    Args:
      start_time: Start time in milliseconds.
      end_time: End time in milliseconds.
      invite_code: Invite code filter.
      page: Result page.
      page_size: Records per page; defaults to 10.
      type_: Commission type: 1 spot, 2 futures, 3 ETF.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#get-affiliate-commission-detail-record-affiliate-only"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if start_time is not None:
      params['startTime'] = ts.dump_ms(start_time)
    if end_time is not None:
      params['endTime'] = ts.dump_ms(end_time)
    if invite_code is not None:
      params['inviteCode'] = invite_code
    if page is not None:
      params['page'] = page
    if page_size is not None:
      params['pageSize'] = page_size
    if type_ is not None:
      params['type'] = type_
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/rebate/affiliate/commission/detail', params=params)
    return self.output(r.text, adapter, validate)

  async def affiliate_commission_detail_paged(self, *, start_time: Timestamp | None = None, end_time: Timestamp | None = None, invite_code: str | None = None, page_size: int | None = None, type_: int | None = None, timestamp: Timestamp | None = None, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[Response200]:
    """Yield pages from `affiliate_commission_detail` until the response reports the final page."""
    page = 1
    while True:
      response = await self.affiliate_commission_detail(start_time=start_time, end_time=end_time, invite_code=invite_code, page_size=page_size, type_=type_, timestamp=timestamp, page=page, validate=validate)
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
