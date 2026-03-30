from typing_extensions import Literal
from dataclasses import dataclass

from typed_core.ws.streams import Stream
from mexc.spot.streams.core import StreamsMixin, Reply
from mexc.spot.streams.core.proto import PublicLimitDepthsV3Api

def channel_name(symbol: str, level: Literal[5, 10, 20]):
  return f'spot@public.limit.depth.v3.api.pb@{symbol}@{level}'
  
@dataclass
class Depth(StreamsMixin):
  async def depth(self, symbol: str, level: Literal[5, 10, 20] = 5) -> Stream[PublicLimitDepthsV3Api, Reply, Reply]:
    """Subscribe to the order book for a given symbol.
    
    - `symbol`: The symbol being traded, e.g. `BTCUSDT`.
    - `level`: The level of the order book (default: 5).

    > [MEXC API docs](https://www.mexc.com/api-docs/spot-v3/websocket-market-streams#partial-book-depth-streams)
    """
    stream = await self.subscribe(channel_name(symbol, level))

    async def parsed_stream():
      async for proto in stream:
        if proto.public_limit_depths is not None:
          yield proto.public_limit_depths

    return Stream(reply=stream.reply, stream=parsed_stream(), unsubscribe=stream.unsubscribe)
