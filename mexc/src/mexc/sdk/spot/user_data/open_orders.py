from dataclasses import dataclass
from decimal import Decimal

from trading_sdk.market.user_data.open_orders import SpotOpenOrders, OrderState

from mexc.core import timestamp
from mexc.sdk.core import SdkMixin, wrap_exceptions, spot_name

@dataclass
class OpenOrders(SpotOpenOrders, SdkMixin):
  @wrap_exceptions
  async def open_orders(self, instrument: str, /) -> list[OrderState]:
    r = await self.client.spot.open_orders(instrument)
    match r:
      case list(orders):
        return [
          OrderState(
            id=o['orderId'],
            price=Decimal(o['price']),
            qty=Decimal(o['origQty']),
            filled_qty=Decimal(o['executedQty']),
            time=timestamp.parse(o['time']),
            side=o['side'],
            status=o['status']
          )
          for o in orders
        ]
      case err:
        raise RuntimeError(err)

  async def spot_open_orders(self, base: str, quote: str, /) -> list[OrderState]:
    instrument = spot_name(base, quote)
    return await self.open_orders(instrument)
