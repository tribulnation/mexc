from typing_extensions import Unpack
from dataclasses import dataclass
import asyncio
import os

from mexc.core.ws.base import SocketClient
from mexc.futures.core import MEXC_FUTURES_API_BASE, AuthHttpClient
from .market_data import MarketData
from .trading import Trading
from .user_data import UserData
from .streams import Streams, MEXC_FUTURES_SOCKET_URL

@dataclass
class Futures(MarketData, Trading, UserData):
  streams: Streams

  def __init__(
    self, *,
    api_url: str = MEXC_FUTURES_API_BASE,
    ws_url: str = MEXC_FUTURES_SOCKET_URL,
    auth_http: AuthHttpClient,
    default_validate: bool = True,
    **kwargs: Unpack[SocketClient.Config],
  ):
    self.base_url = api_url
    self.default_validate = default_validate
    self.http = self.auth_http = auth_http
    self.streams = Streams.new(
      auth_http.api_key, auth_http.api_secret,
      url=ws_url,
      default_validate=default_validate,
      **kwargs,
    )

  @classmethod
  def new(
    cls, api_key: str | None = None, api_secret: str | None = None, *,
    base_url: str = MEXC_FUTURES_API_BASE,
    ws_url: str = MEXC_FUTURES_SOCKET_URL,
    default_validate: bool = True,
    **kwargs: Unpack[SocketClient.Config],
  ):
    if api_key is None:
      api_key = os.environ['MEXC_ACCESS_KEY']
    if api_secret is None:
      api_secret = os.environ['MEXC_SECRET_KEY']
    auth_http = AuthHttpClient(api_key=api_key, api_secret=api_secret)
    return cls(api_url=base_url, ws_url=ws_url, auth_http=auth_http, default_validate=default_validate, **kwargs)
  
  async def __aexit__(self, exc_type, exc_value, traceback):
    await asyncio.gather(
      super().__aexit__(exc_type, exc_value, traceback),
      self.streams.__aexit__(exc_type, exc_value, traceback),
    )
