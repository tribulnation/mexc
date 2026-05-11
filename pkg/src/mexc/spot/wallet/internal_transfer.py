from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Response200(TypedDict):
  """Internal transfer response."""
  tranId: NotRequired[str | None]
  """Transfer id."""

Response: type[Response200 | ErrorResponse] = Response200 | ErrorResponse # type: ignore
adapter = validator(Response)

class InternalTransfer(AuthSpotMixin):
  async def internal_transfer(
    self,
    *,
    to_account_type: str,
    to_account: str,
    area_code: str | None = None,
    asset: str,
    amount: str,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> Response200:
    """Transfers assets internally to another MEXC account by email, UID, or mobile number.

    Args:
      to_account_type: Recipient account identifier type: EMAIL, UID, or MOBILE.
      to_account: Recipient email, UID, or mobile number.
      area_code: Area code when using a mobile recipient.
      asset: Asset to transfer.
      amount: Transfer amount.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#internal-transfer"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if to_account_type is not None:
      params['toAccountType'] = to_account_type
    if to_account is not None:
      params['toAccount'] = to_account
    if area_code is not None:
      params['areaCode'] = area_code
    if asset is not None:
      params['asset'] = asset
    if amount is not None:
      params['amount'] = amount
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('POST', '/api/v3/capital/transfer/internal', params=params)
    return self.output(r.text, adapter, validate)
