from dataclasses import dataclass

from trading_sdk.types import fmt_num, ApiError
from trading_sdk.market.trading.place_order import SpotPlaceOrder, Order as OrderTDK

from mexc.spot.trading.place_order import Order, LimitOrder, MarketOrder
from mexc.sdk.core import SdkMixin, wrap_exceptions, spot_name

def parse_order(order: OrderTDK) -> Order:
  if order['type'] == 'LIMIT':
    return LimitOrder(
      type='LIMIT',
      side=order['side'],
      price=fmt_num(order['price']),
      quantity=fmt_num(order['qty'])
    )
  elif order['type'] == 'MARKET':
    return MarketOrder(
      type='MARKET',
      side=order['side'],
      quantity=fmt_num(order['qty'])
    )

@dataclass
class PlaceOrder(SpotPlaceOrder, SdkMixin):
  @wrap_exceptions
  async def place_order(self, instrument: str, /, order: OrderTDK) -> str:
    r = await self.client.spot.place_order(instrument, parse_order(order))
    if 'code' in r:
      raise ApiError(r)
    else:
      return r['orderId']

  async def spot_place_order(self, base: str, quote: str, /, order: OrderTDK) -> str:
    instrument = spot_name(base, quote)
    return await self.place_order(instrument, order)
  