from typing_extensions import TypedDict, NotRequired
from pydantic import RootModel
from mexc.core import AuthedMixin, timestamp as ts, ApiError

class Chain(TypedDict):
  coin: str
  network: str
  address: str
  chainName: str
  chainDisplayName: str
  """New standard naming, use this for withdraws."""
  netWork: str
  memo: NotRequired[str | None]

class Response(RootModel):
  root: list[Chain] | ApiError

class DepositAddresses(AuthedMixin):
  async def deposit_addresses(
    self, coin: str, *, network: str | None = None,
    timestamp: int | None = None, validate: bool = True,
  ) -> ApiError | list[Chain]:
    """Get deposit addresses for a given coin.
    
    - `coin`: The coin to get the deposit addresses for, e.g. `USDT`.
    - `network`: The network to get the deposit addresses for, e.g. `Tron(TRC20)`. If not given, returns all networks. 
    - `timestamp`: The timestamp for the request, in milliseconds (default: now).
    - `validate`: Whether to validate the response against the expected schema (default: True).

    > [MEXC API docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/#deposit-address-supporting-network)
    """
    params = {
      'coin': coin, 'timestamp': timestamp or ts.now()
    }
    if network is not None:
      params['network'] = network
    r = await self.signed_request('GET', '/api/v3/capital/deposit/address', params)
    return Response.model_validate_json(r.text).root if validate else r.json()
