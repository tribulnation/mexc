from dataclasses import dataclass as _dataclass
import asyncio

from mexc.spot.core import MEXC_SPOT_API_BASE, AuthHttpClient
from .core import StreamsClient, UserStreamsClient, MEXC_SPOT_SOCKET_URL
from .market import MarketStreams
from .user import UserStreams

@_dataclass
class Streams(MarketStreams, UserStreams):

  def __init__(
    self, *,
    api_url: str = MEXC_SPOT_API_BASE,
    ws_url: str = MEXC_SPOT_SOCKET_URL,
    auth_http: AuthHttpClient,
  ):
    self.ws = StreamsClient(url=ws_url)
    self.auth_ws = UserStreamsClient(auth_http=auth_http, api_url=api_url, ws_url=ws_url)

  @classmethod
  def new(
    cls, api_key: str | None = None, api_secret: str | None = None, *,
    api_url: str = MEXC_SPOT_API_BASE,
    ws_url: str = MEXC_SPOT_SOCKET_URL,
  ):
    import os
    if api_key is None:
      api_key = os.environ['MEXC_ACCESS_KEY']
    if api_secret is None:
      api_secret = os.environ['MEXC_SECRET_KEY']
    auth_http = AuthHttpClient(api_key=api_key, api_secret=api_secret)
    return cls(api_url=api_url, ws_url=ws_url, auth_http=auth_http)

  async def __aenter__(self):
    await asyncio.gather(
      self.ws.__aenter__(),
      self.auth_ws.__aenter__(),
    )
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    tasks = []
    if self.ws.ctx_future.done():
      tasks.append(self.ws.__aexit__(exc_type, exc_value, traceback))
    if self.auth_ws.ctx_future.done():
      tasks.append(self.auth_ws.__aexit__(exc_type, exc_value, traceback))
    if tasks:
      await asyncio.gather(*tasks)
  
