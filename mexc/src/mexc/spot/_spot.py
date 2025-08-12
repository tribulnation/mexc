from typing_extensions import Unpack
from dataclasses import dataclass
from mexc.core import AuthHttpClient
from mexc.spot import MEXC_SPOT_API_BASE
from .market_data import MarketData
from .trading import Trading
from .user_data import UserData
from .streams import Streams, MEXC_SOCKET_URL

@dataclass
class Spot(MarketData, Trading, UserData):
  streams: Streams

  def __init__(
    self, *,
    api_url: str = MEXC_SPOT_API_BASE,
    ws_url: str = MEXC_SOCKET_URL,
    auth_http: AuthHttpClient,
    default_validate: bool = True,
    **kwargs: Unpack[Streams.Config],
  ):
    self.default_validate = default_validate
    self.base_url = api_url
    self.http = self.auth_http = auth_http
    self.streams = Streams(api_url=api_url, ws_url=ws_url, auth_http=auth_http, **kwargs)