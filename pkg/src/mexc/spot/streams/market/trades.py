from typing_extensions import Literal
from dataclasses import dataclass

from typed_core.ws.streams import Stream
from mexc.spot.streams.core import StreamsMixin, Reply
from mexc.spot.streams.core.proto import PublicAggreDealsV3Api

Aggregation = Literal['100ms', '10ms']

def channel_name(symbol: str, aggregation: Aggregation):
  return f'spot@public.aggre.deals.v3.api.pb@{aggregation}@{symbol}'

@dataclass
class Trades(StreamsMixin):
  async def trades(
    self, symbol: str, aggregation: Aggregation = '100ms',
  ) -> Stream[PublicAggreDealsV3Api, Reply, Reply]:
    """
    Subscribe to aggregated spot trade updates.

    Args:
      symbol: Spot symbol, for example `BTCUSDT`.
      aggregation: Update aggregation interval.

    References:
      - [MEXC spot WebSocket market streams](https://www.mexc.com/api-docs/spot-v3/websocket-market-streams#trade-streams)
    """
    stream = await self.subscribe(channel_name(symbol, aggregation))

    async def parsed_stream():
      async for proto in stream:
        if proto.public_aggre_deals is not None:
          yield proto.public_aggre_deals

    return Stream(reply=stream.reply, stream=parsed_stream(), unsubscribe=stream.unsubscribe)
