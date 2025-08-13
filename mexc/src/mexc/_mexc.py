from dataclasses import dataclass
import asyncio
from mexc.core import AuthHttpClient
from .spot import Spot
from .futures import Futures

@dataclass
class MEXC:
  spot: Spot
  futures: Futures

  @classmethod
  def new(
    cls, api_key: str, api_secret: str, *,
    validate: bool = True,
  ):
    auth_http = AuthHttpClient(api_key, api_secret)
    return cls(
      spot=Spot(auth_http=auth_http, default_validate=validate),
      futures=Futures(auth_http=auth_http, default_validate=validate),
    )
  
  @classmethod
  def env(cls, *, validate: bool = True):
    import os
    return cls.new(api_key=os.environ['MEXC_ACCESS_KEY'], api_secret=os.environ['MEXC_SECRET_KEY'], validate=validate)

  async def __aenter__(self):
    await asyncio.gather(
      self.spot.__aenter__(),
      self.futures.__aenter__(),
    )
    return self
  
  async def __aexit__(self, exc_type, exc_value, traceback):
    await asyncio.gather(
      self.spot.__aexit__(exc_type, exc_value, traceback),
      self.futures.__aexit__(exc_type, exc_value, traceback),
    )