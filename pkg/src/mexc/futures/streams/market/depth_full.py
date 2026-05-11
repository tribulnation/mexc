from dataclasses import dataclass
from typing_extensions import Literal

from typed_core.ws.streams import Stream
from mexc.futures.streams.core import StreamsMixin, Reply
from .depth import Depth, validate_response

DepthLimit = Literal[5, 10, 20]

@dataclass
class DepthFull(StreamsMixin):
  async def depth_full(
    self, symbol: str, *, limit: DepthLimit = 20, validate: bool = True,
  ) -> Stream[Depth, Reply, Reply]:
    """
    Subscribe to futures full-depth snapshots.

    Args:
      symbol: Futures contract symbol, for example `BTC_USDT`.
      limit: Number of price levels in each snapshot.
      validate: Validate pushed depth payloads.

    References:
      - [MEXC futures WebSocket API](https://mexcdevelop.github.io/apidocs/contract_v1_en/#filter-subscription)
    """
    stream = await self.subscribe('depth.full', {'symbol': symbol, 'limit': limit})
    async def parsed_stream():
      async for msg in stream:
        yield validate_response(msg) if self.validate(validate) else msg
    return Stream(reply=stream.reply, stream=parsed_stream(), unsubscribe=stream.unsubscribe)
