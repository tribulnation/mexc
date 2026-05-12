from datetime import datetime
from typing_extensions import AsyncIterator, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class AffiliateSubaffiliatesItem(TypedDict):
  """Affiliate record."""
  subaffiliateName: str
  """Sub-affiliate display name."""
  subaffiliateMail: str
  """Masked sub-affiliate email."""
  campaign: str | None
  """Campaign name."""
  inviteCode: str
  """Invite code."""
  activationTime: datetime
  """Sub-affiliate activation time."""
  registered: int
  """Registered-user count."""
  deposited: int
  """Deposited-user count."""
  depositAmount: str
  """Deposit amount."""
  commission: str
  """Commission amount."""

class AffiliateSubaffiliatesData(TypedDict):
  """Paginated affiliate data."""
  pageSize: int
  """Number of records requested per page."""
  totalCount: int
  """Total number of matching records."""
  totalPage: int
  """Total number of result pages."""
  currentPage: int
  """Current result page."""
  resultList: list[AffiliateSubaffiliatesItem]
  """Affiliate records for the page."""

class AffiliateSubaffiliatesResponse(TypedDict):
  """Affiliate wrapper response."""
  success: bool
  """Whether the request succeeded."""
  code: int
  """Business response code."""
  message: str | None
  """Business response message."""
  data: AffiliateSubaffiliatesData

Response: type[AffiliateSubaffiliatesResponse | ErrorResponse] = AffiliateSubaffiliatesResponse | ErrorResponse # type: ignore
adapter = validator(Response)

class AffiliateSubaffiliates(AuthSpotMixin):
  async def affiliate_subaffiliates(
    self,
    *,
    start_time: Timestamp | None = None,
    end_time: Timestamp | None = None,
    invite_code: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> AffiliateSubaffiliatesResponse:
    """Affiliate-only endpoint returning sub-affiliate activation, registration, deposit, campaign, and commission data.

    Args:
      start_time: Start time in milliseconds.
      end_time: End time in milliseconds.
      invite_code: Invite code filter.
      page: Result page.
      page_size: Records per page; defaults to 10.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#get-subaffiliates-data-affiliate-only)
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
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('GET', '/api/v3/rebate/affiliate/subaffiliates', params=params)
    return self.output(r.text, adapter, validate)

  async def affiliate_subaffiliates_paged(self, *, start_time: Timestamp | None = None, end_time: Timestamp | None = None, invite_code: str | None = None, page_size: int | None = None, timestamp: Timestamp | None = None, max_pages: int | None = None, validate: bool | None = None) -> AsyncIterator[AffiliateSubaffiliatesResponse]:
    """Yield pages from `affiliate_subaffiliates` until the response reports the final page."""
    page = 1
    while True:
      response = await self.affiliate_subaffiliates(start_time=start_time, end_time=end_time, invite_code=invite_code, page_size=page_size, timestamp=timestamp, page=page, validate=validate)
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
