from dataclasses import dataclass as _dataclass
import asyncio as _asyncio

from .spot import Spot
from .spot.core import MEXC_SPOT_API_BASE as _MEXC_SPOT_API_BASE
from .spot.streams.core import MEXC_SPOT_SOCKET_URL as _MEXC_SPOT_SOCKET_URL
from .futures import Futures
from .futures.core import MEXC_FUTURES_API_BASE as _MEXC_FUTURES_API_BASE
from .futures.streams.core import MEXC_FUTURES_SOCKET_URL as _MEXC_FUTURES_SOCKET_URL
from .core import ApiError, AuthError, BadRequest, Error, LogicError, NetworkError, RateLimited, ValidationError
from . import spot, futures, core

@_dataclass
class MEXC:
  spot: Spot
  futures: Futures

  @classmethod
  def new(
    cls, api_key: str | None = None, api_secret: str | None = None, *,
    validate: bool = True,
    spot_base_url: str = _MEXC_SPOT_API_BASE,
    spot_ws_url: str = _MEXC_SPOT_SOCKET_URL,
    futures_base_url: str = _MEXC_FUTURES_API_BASE,
    futures_ws_url: str = _MEXC_FUTURES_SOCKET_URL,
  ):
    return cls(
      spot=Spot.new(
        api_key=api_key,
        api_secret=api_secret,
        base_url=spot_base_url,
        ws_url=spot_ws_url,
        default_validate=validate,
      ),
      futures=Futures.new(
        api_key=api_key,
        api_secret=api_secret,
        base_url=futures_base_url,
        ws_url=futures_ws_url,
        default_validate=validate,
      ),
    )

  @classmethod
  def public(
    cls, *,
    validate: bool = True,
    spot_base_url: str = _MEXC_SPOT_API_BASE,
    spot_ws_url: str = _MEXC_SPOT_SOCKET_URL,
    futures_base_url: str = _MEXC_FUTURES_API_BASE,
    futures_ws_url: str = _MEXC_FUTURES_SOCKET_URL,
  ):
    return cls(
      spot=Spot.public(
        base_url=spot_base_url,
        ws_url=spot_ws_url,
        default_validate=validate,
      ),
      futures=Futures.public(
        base_url=futures_base_url,
        ws_url=futures_ws_url,
        default_validate=validate,
      ),
    )

  async def __aenter__(self):
    await _asyncio.gather(
      self.spot.__aenter__(),
      self.futures.__aenter__(),
    )
    return self
  
  async def __aexit__(self, exc_type, exc_value, traceback):
    await _asyncio.gather(
      self.spot.__aexit__(exc_type, exc_value, traceback),
      self.futures.__aexit__(exc_type, exc_value, traceback),
    )
