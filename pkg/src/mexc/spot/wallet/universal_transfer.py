from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class Item(TypedDict):
  """Universal transfer result."""
  tranId: NotRequired[str | None]
  """Transfer id."""

Response: type[list[Item] | ErrorResponse] = list[Item] | ErrorResponse # type: ignore
adapter = validator(Response)

class UniversalTransfer(AuthSpotMixin):
  async def universal_transfer(
    self,
    *,
    from_account_type: str,
    to_account_type: str,
    asset: str,
    amount: str,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> list[Item]:
    """Transfers assets between the signed user account types such as spot and futures.

    Args:
      from_account_type: Source account type, such as SPOT or FUTURES.
      to_account_type: Destination account type, such as SPOT or FUTURES.
      asset: Asset to transfer.
      amount: Transfer amount.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      Upstream docs: https://mexcdevelop.github.io/apidocs/spot_v3_en/#user-universal-transfer"""
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if from_account_type is not None:
      params['fromAccountType'] = from_account_type
    if to_account_type is not None:
      params['toAccountType'] = to_account_type
    if asset is not None:
      params['asset'] = asset
    if amount is not None:
      params['amount'] = amount
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('POST', '/api/v3/capital/transfer', params=params)
    return self.output(r.text, adapter, validate)
