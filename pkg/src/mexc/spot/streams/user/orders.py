from dataclasses import dataclass

from typed_core.ws.streams import Stream
from mexc.spot.streams.core import UserStreamsMixin, Reply
from mexc.spot.streams.core.proto import PrivateOrdersV3Api

@dataclass
class Orders(UserStreamsMixin):
  async def orders(self) -> Stream[PrivateOrdersV3Api, Reply, Reply]:
    """
    Subscribe to spot order updates.

    References:
      - [MEXC spot WebSocket user streams](https://www.mexc.com/api-docs/spot-v3/websocket-user-data-streams#spot-account-orders)
    """
    stream = await self.authed_subscribe('spot@private.orders.v3.api.pb')

    async def parsed_stream():
      async for proto in stream:
        if proto.private_orders is not None:
          yield proto.private_orders

    return Stream(reply=stream.reply, stream=parsed_stream(), unsubscribe=stream.unsubscribe)
