from dataclasses import dataclass
import os
import asyncio

from .core import StreamsClient, AuthedStreamsClient, MEXC_FUTURES_SOCKET_URL
from .user import UserStreams
from .market import MarketStreams

@dataclass
class Streams(
  UserStreams,
  MarketStreams,
):
  @classmethod
  def new(
    cls, api_key: str | None = None, api_secret: str | None = None, *,
    url: str = MEXC_FUTURES_SOCKET_URL,
    default_validate: bool = True,
  ):
    if api_key is None:
      api_key = os.environ['MEXC_ACCESS_KEY']
    if api_secret is None:
      api_secret = os.environ['MEXC_SECRET_KEY']
    ws = StreamsClient(url=url)
    auth_ws = AuthedStreamsClient(api_key=api_key, api_secret=api_secret, url=url)
    return cls(auth_ws=auth_ws, ws=ws, default_validate=default_validate)

  async def __aenter__(self):
    await self.auth_ws.__aenter__()
    await self.ws.__aenter__()
    return self
  
  async def __aexit__(self, exc_type, exc_value, traceback):
    tasks = []
    if self.auth_ws.ctx_future.done():
      tasks.append(self.auth_ws.__aexit__(exc_type, exc_value, traceback))
    if self.ws.ctx_future.done():
      tasks.append(self.ws.__aexit__(exc_type, exc_value, traceback))
    if tasks:
      await asyncio.gather(*tasks)
  
