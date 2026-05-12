from datetime import datetime
from typing_extensions import NotRequired, TypedDict
from mexc.spot.core import ErrorResponse, SpotMixin
from mexc.core import validator

class EtfInfoResponse(TypedDict):
  """ETF information."""
  symbol: NotRequired[str]
  """ETF symbol."""
  netValue: NotRequired[str | float]
  """Current net value."""
  leverage: NotRequired[str | float]
  """ETF leverage multiplier."""
  fundFee: NotRequired[str | float]
  """Fund fee rate."""
  fundFeeTime: NotRequired[datetime]
  """Fund fee timestamp in milliseconds."""
  basket: NotRequired[str]
  """Underlying basket description."""

class EtfInfoListItem(TypedDict):
  """ETF information."""
  symbol: NotRequired[str]
  """ETF symbol."""
  netValue: NotRequired[str | float]
  """Current net value."""
  leverage: NotRequired[str | float]
  """ETF leverage multiplier."""
  fundFee: NotRequired[str | float]
  """Fund fee rate."""
  fundFeeTime: NotRequired[datetime]
  """Fund fee timestamp in milliseconds."""
  basket: NotRequired[str]
  """Underlying basket description."""

Response: type[EtfInfoResponse | list[EtfInfoListItem] | ErrorResponse] = EtfInfoResponse | list[EtfInfoListItem] | ErrorResponse # type: ignore
adapter = validator(Response)

class EtfInfo(SpotMixin):
  async def etf_info(
    self,
    *,
    symbol: str | None = None,
    validate: bool | None = None
  ) -> EtfInfoResponse | list[EtfInfoListItem]:
    """Return spot ETF information such as net value, leverage, and fund fee.

    Args:
      symbol: ETF symbol.
      validate: Validation override for this request.

    Returns:
      The validated endpoint response.

    References:
      - [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#etf-endpoints)
    """
    params = {}
    if symbol is not None:
      params['symbol'] = symbol
    r = await self.request('GET', '/api/v3/etf/info', params=params)
    return self.output(r.text, adapter, validate)
