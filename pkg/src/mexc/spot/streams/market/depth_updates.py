from typing_extensions import Literal
from dataclasses import dataclass

from typed_core.ws.streams import Stream
from mexc.spot.streams.core import StreamsMixin, Reply
from mexc.spot.streams.core.proto import PublicAggreDepthsV3Api

Aggregation = Literal['100ms', '10ms']

def channel_name(symbol: str, aggregation: Aggregation):
  return f'spot@public.aggre.depth.v3.api.pb@{aggregation}@{symbol}'
  
@dataclass
class DepthUpdates(StreamsMixin):
  async def depth_updates(
    self, symbol: str, aggregation: Aggregation = '10ms',
  ) -> Stream[PublicAggreDepthsV3Api, Reply, Reply]:
    """
    Subscribe to aggregated spot order-book delta updates.

    Args:
      symbol: Spot symbol, for example `BTCUSDT`.
      aggregation: Update aggregation interval.

    References:
      - [MEXC spot WebSocket market streams](https://www.mexc.com/api-docs/spot-v3/websocket-market-streams#diffdepth-stream)
      - [Maintaining a local order book](https://www.mexc.com/api-docs/spot-v3/websocket-market-streams#how-to-properly-maintain-a-local-copy-of-the-order-book)
    """
    stream = await self.subscribe(channel_name(symbol, aggregation))

    async def parsed_stream():
      async for proto in stream:
        if proto.public_aggre_depths is not None:
          yield proto.public_aggre_depths

    return Stream(reply=stream.reply, stream=parsed_stream(), unsubscribe=stream.unsubscribe)
