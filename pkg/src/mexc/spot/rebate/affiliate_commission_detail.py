from typing_extensions import AsyncIterator, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class AffiliateCommissionDetailItem(TypedDict):
  """Affiliate record."""
  type: int
  """Commission type: 1 spot, 2 futures, 3 ETF."""
  sourceType: int
  """Source type: 1 referral, 2 sub-affiliate."""
  state: int
  """Commission state."""
  date: int
  """Trade date."""
  uid: str
  """User id."""
  rate: float | str
  """Commission rate."""
  symbol: str
  """Trading symbol."""
  takerAmount: str
  """Taker trade amount."""
  makerAmount: str
  """Maker trade amount."""
  amountCurrency: str
  """Trade amount currency."""
  usdtAmount: str
  """USDT trade amount."""
  commission: str
  """Commission amount."""
  currency: str
  """Commission currency."""

class AffiliateCommissionDetailData(TypedDict):
  """Paginated affiliate data."""
  pageSize: int
  """Number of records requested per page."""
  totalCount: int
  """Total number of matching records."""
  totalPage: int
  """Total number of result pages."""
  currentPage: int
  """Current result page."""
  resultList: list[AffiliateCommissionDetailItem]
  """Affiliate records for the page."""
  totalCommissionUsdtAmount: str
  """Total commission in USDT."""
  totalTradeUsdtAmount: str
  """Total trade volume in USDT."""

class AffiliateCommissionDetailResponse(TypedDict):
  """Affiliate wrapper response."""
  success: bool
  """Whether the request succeeded."""
  code: int
  """Business response code."""
  message: str | None
  """Business response message."""
  data: AffiliateCommissionDetailData

Response: type[AffiliateCommissionDetailResponse | ErrorResponse] = AffiliateCommissionDetailResponse | ErrorResponse # type: ignore
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
  ) -> AffiliateCommissionDetailResponse:
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
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#get-affiliate-commission-detail-record-affiliate-only)
    """
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

  async def affiliate_commission_detail_paged(self, *, start_time: Timestamp | None = None, end_time: Timestamp | None = None, invite_code: str | None = None, page_size: int | None = None, type_: int | None = None, timestamp: Timestamp | None = None, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[AffiliateCommissionDetailResponse]:
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
