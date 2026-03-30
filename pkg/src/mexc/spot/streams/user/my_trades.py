from dataclasses import dataclass

from typed_core.ws.streams import Stream
from mexc.spot.streams.core import UserStreamsMixin, Reply
from mexc.spot.streams.core.proto import PrivateDealsV3Api

@dataclass
class MyTrades(UserStreamsMixin):
  async def my_trades(self) -> Stream[PrivateDealsV3Api, Reply, Reply]:
    """Subscribe to your trades.
    
    > [MEXC API docs](https://www.mexc.com/api-docs/spot-v3/websocket-user-data-streams#spot-account-deals)
    """
    stream = await self.authed_subscribe('spot@private.deals.v3.api.pb')
    async def parsed_stream():
      async for proto in stream:
        if proto.private_deals is not None:
          yield proto.private_deals
    return Stream(reply=stream.reply, stream=parsed_stream(), unsubscribe=stream.unsubscribe)
