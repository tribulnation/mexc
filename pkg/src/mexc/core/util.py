from typing_extensions import TypeAlias, TypeVar, Mapping, Callable, Awaitable
import time
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_DOWN, ROUND_FLOOR

T = TypeVar('T')
D = TypeVar('D', bound=Mapping)
Timestamp: TypeAlias = datetime | int

def filter_kwargs(Params: type[D], params: D | dict) -> D:
  return { k: params[k] for k in getattr(Params, '__annotations__', {}) if k in params } # type: ignore

class timestamp:
  @staticmethod
  def parse(time: int) -> datetime:
    return datetime.fromtimestamp(time/1e3)
  
  @staticmethod
  def dump(dt: datetime) -> int:
    return int(1e3*dt.timestamp())

  @staticmethod
  def dump_ms(value: Timestamp) -> int:
    if isinstance(value, datetime):
      return int(1e3*value.timestamp())
    return value

  @staticmethod
  def dump_s(value: Timestamp) -> int:
    if isinstance(value, datetime):
      return int(value.timestamp())
    return value
  
  @staticmethod
  def now() -> int:
    return int(time.time() * 1e3)

def round2tick(x: Decimal, tick_size: Decimal) -> Decimal:
  r = (x / tick_size).quantize(Decimal('1.'), rounding=ROUND_HALF_DOWN) * tick_size
  return r.normalize()

def trunc2tick(x: Decimal, tick_size: Decimal) -> Decimal:
  r = (x / tick_size).to_integral_value(rounding=ROUND_FLOOR) * tick_size
  return r.normalize()
