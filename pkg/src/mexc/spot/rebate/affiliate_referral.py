from datetime import datetime
from typing_extensions import AsyncIterator, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class AffiliateReferralItem(TypedDict):
  """Affiliate record."""
  uid: int | str
  """Referral user id."""
  nickName: str | None
  """Referral nickname."""
  email: str
  """Referral email."""
  registerTime: datetime
  """Registration time."""
  inviteCode: str
  """Invite code."""
  depositAmount: str
  """Deposit amount in USDT."""
  tradingAmount: str
  """Trading amount in USDT."""
  commission: str
  """Commission amount in USDT."""
  firstDepositTime: datetime | None
  """First deposit time."""
  firstTradeTime: datetime | None
  """First trade time."""
  lastDepositTime: datetime | None
  """Last deposit time."""
  lastTradeTime: datetime | None
  """Last trade time."""
  withdrawAmount: str
  """Withdrawal amount in USDT."""
  asset: str
  """Asset balance band."""
  identification: int
  """KYC identification level."""

class AffiliateReferralData(TypedDict):
  """Paginated affiliate data."""
  pageSize: int
  """Number of records requested per page."""
  totalCount: int
  """Total number of matching records."""
  totalPage: int
  """Total number of result pages."""
  currentPage: int
  """Current result page."""
  resultList: list[AffiliateReferralItem]
  """Affiliate records for the page."""

class AffiliateReferralResponse(TypedDict):
  """Affiliate wrapper response."""
  success: bool
  """Whether the request succeeded."""
  code: int
  """Business response code."""
  message: str | None
  """Business response message."""
  data: AffiliateReferralData

Response: type[AffiliateReferralResponse | ErrorResponse] = AffiliateReferralResponse | ErrorResponse # type: ignore
adapter = validator(Response)

class AffiliateReferral(AuthSpotMixin):
  async def affiliate_referral(
    self,
    *,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    uid: str | None = None,
    invite_code: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> AffiliateReferralResponse:
    """Affiliate-only endpoint returning referred-user deposit, trading, commission, asset-band, and identification data.

    Args:
      start_time: Start time in milliseconds.
      end_time: End time in milliseconds.
      uid: Referral user id filter.
      invite_code: Invite code filter.
      page: Result page.
      page_size: Records per page; defaults to 10.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#get-affiliate-referral-data-affiliate-only)
    """
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if start_time is not None:
      params['startTime'] = ts.dump_ms(start_time)
    if end_time is not None:
      params['endTime'] = ts.dump_ms(end_time)
    if uid is not None:
      params['uid'] = uid
    if invite_code is not None:
      params['inviteCode'] = invite_code
    if page is not None:
      params['page'] = page
    if page_size is not None:
      params['pageSize'] = page_size
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/rebate/affiliate/referral', params=params)
    return self.output(r.text, adapter, validate)

  async def affiliate_referral_paged(self, *, start_time: Timestamp | None = None, end_time: Timestamp | None = None, uid: str | None = None, invite_code: str | None = None, page_size: int | None = None, timestamp: Timestamp | None = None, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[AffiliateReferralResponse]:
    """Yield pages from `affiliate_referral` until the response reports the final page."""
    page = 1
    while True:
      response = await self.affiliate_referral(start_time=start_time, end_time=end_time, uid=uid, invite_code=invite_code, page_size=page_size, timestamp=timestamp, page=page, validate=validate)
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
