from dataclasses import dataclass
from decimal import Decimal

from typed_core.ws.streams import Stream
from mexc.core import validator, TypedDict
from mexc.futures.streams.core import StreamsMixin, Reply

class AllTicker(TypedDict, total=False):
  symbol: str
  lastPrice: Decimal
  volume24: Decimal
  riseFallRate: Decimal
  fairPrice: Decimal

validate_response = validator(list[AllTicker])

@dataclass
class Tickers(StreamsMixin):
  async def all_tickers(self, *, validate: bool = True) -> Stream[list[AllTicker], Reply, Reply]:
    """
    Subscribe to ticker updates for all futures contracts.

    Args:
      validate: Validate pushed ticker payloads.

    References:
      - [MEXC futures WebSocket API](https://mexcdevelop.github.io/apidocs/contract_v1_en/#filter-subscription)
    """
    stream = await self.subscribe('tickers')
    async def parsed_stream():
      async for msg in stream:
        yield validate_response(msg) if self.validate(validate) else msg
    return Stream(reply=stream.reply, stream=parsed_stream(), unsubscribe=stream.unsubscribe)

  async def tickers(self, *, validate: bool = True) -> Stream[list[AllTicker], Reply, Reply]:
    """
    Subscribe to ticker updates for all futures contracts.

    Args:
      validate: Validate pushed ticker payloads.
    """
    return await self.all_tickers(validate=validate)
