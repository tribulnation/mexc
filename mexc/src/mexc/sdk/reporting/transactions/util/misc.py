from typing_extensions import Literal, Iterable, Protocol
from datetime import datetime, timezone

from trading_sdk.reporting import Operation

class Module(Protocol):
  matching_mode: Literal['eq', 'ge']

  def parse(self, path: str, tz: timezone, /, *, skip_zero_changes: bool = True) -> Iterable[Operation]:
    ...

def ensure_datetime(x) -> datetime:
  return x if isinstance(x, datetime) else datetime.fromisoformat(str(x))