from pydantic import RootModel
from mexc.core import AuthedMixin, timestamp as ts, ApiError
from .query_order import OrderState

class Response(RootModel):
  root: list[OrderState] | ApiError

class QueryAllOrders(AuthedMixin):
  async def query_all_orders(
    self, *, symbol: str,
    recvWindow: int | None = None,
    timestamp: int | None = None,
    validate: bool = True,
  ) -> ApiError | list[OrderState]:
    """Query all orders (of your account) for a given symbol.
    
    - `symbol`: The symbol being traded, e.g. `BTCUSDT`
    - `recvWindow`: If the server receives the request after `timestamp + recvWindow`, it will be rejected (default: 5000).
    - `timestamp`: The timestamp for the request, in milliseconds (default: now).
    - `validate`: Whether to validate the response against the expected schema (default: True).

    > [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#all-orders)
    """
    params = {
      'symbol': symbol,
      'timestamp': timestamp or ts.now(),
    }
    if recvWindow is not None:
      params['recvWindow'] = recvWindow
    r = await self.signed_request('GET', '/api/v3/openOrders', params)
    return Response.model_validate_json(r.text).root if validate else r.json()