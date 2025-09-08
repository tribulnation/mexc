from dataclasses import dataclass
from decimal import Decimal
from trading_sdk.types import ApiError

from trading_sdk.market.user_data.query_order import SpotQueryOrder, OrderState

from mexc.core import timestamp
from mexc.sdk.core import SdkMixin, wrap_exceptions, spot_name

@dataclass
class QueryOrder(SpotQueryOrder, SdkMixin):
  @wrap_exceptions
  async def query_order(self, instrument: str, /, *, id: str) -> OrderState:
    r = await self.client.spot.query_order(instrument, orderId=id)
    if 'code' in r:
      raise ApiError(r)
    else:
      return OrderState(
        id=r['orderId'],
        price=Decimal(r['price']),
        qty=Decimal(r['origQty']),
        filled_qty=Decimal(r['executedQty']),
        time=timestamp.parse(r['time']),
        side=r['side'],
        status=r['status']
      )

  async def spot_query_order(self, base: str, quote: str, /, *, id: str) -> OrderState:
    instrument = spot_name(base, quote)
    return await self.query_order(instrument, id=id)