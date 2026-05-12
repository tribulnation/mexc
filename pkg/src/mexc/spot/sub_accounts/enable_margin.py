from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import AuthSpotMixin, ErrorResponse
from mexc.core import Timestamp, timestamp as ts, validator

class EnableMarginRequest(TypedDict):
  subAccount: NotRequired[str]
  """Sub-account name whose margin capability should be enabled."""

class EnableMarginResponse(TypedDict):
  """Sub-account margin enablement result."""
  subAccount: NotRequired[str]
  """Sub-account name."""
  isMarginEnabled: NotRequired[bool]
  """Whether margin has been enabled."""
  code: NotRequired[int]
  """MEXC response code when returned."""
  msg: NotRequired[str | None]
  """Status message when returned."""

Response: type[EnableMarginResponse | ErrorResponse] = EnableMarginResponse | ErrorResponse # type: ignore
adapter = validator(Response)

class EnableMargin(AuthSpotMixin):
  async def enable_margin(
    self,
    *,
    sub_account: str,
    timestamp: Timestamp | None = None,
    validate: bool | None = None
  ) -> EnableMarginResponse:
    """Enables margin capability for a sub-account. The exact endpoint is docs-ambiguous because the current official Spot V3 page omits this operation.

    Args:
      sub_account: Sub-account name whose margin capability should be enabled. Parameter inferred from the requested endpoint because current Spot docs omit this operation.
      timestamp: Signed request timestamp in milliseconds.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#sub-account-endpoints)
    """
    if timestamp is None:
      timestamp = ts.now()
    params = {}
    if sub_account is not None:
      params['subAccount'] = sub_account
    if timestamp is not None:
      params['timestamp'] = ts.dump_ms(timestamp)
    r = await self.signed_request('POST', '/api/v3/sub-account/margin', params=params)
    return self.output(r.text, adapter, validate)
