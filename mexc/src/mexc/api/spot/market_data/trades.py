from typing_extensions import TypedDict
from pydantic import RootModel
from mexc.core import ClientMixin, ApiError

class Trade(TypedDict):
  id: str | None
  price: str
  qty: str
  quoteQty: str
  time: int
  isBuyerMaker: bool
  isBestMatch: bool

class Response(RootModel):
  root: list[Trade] | ApiError

class Trades(ClientMixin):
  async def trades(
    self, symbol: str, *,
    limit: int | None = None,
    validate: bool = True,
  ) -> ApiError | list[Trade]:
    """Get recent trades for a given symbol.
    
    - `symbol`: The symbol being traded, e.g. `BTCUSDT`.
    - `limit`: The maximum number of trades to return (default: 500, max: 1000).
    - `validate`: Whether to validate the response against the expected schema (default: True).

    > [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#recent-trades-list)
    """
    params: dict = {'symbol': symbol}
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', '/api/v3/trades', params=params)
    return Response.model_validate_json(r.text).root if validate else r.json()