from typing_extensions import AsyncIterable
from dataclasses import dataclass
from datetime import datetime, timezone
import os

from trading_sdk.reporting import (
  Transaction, Transactions as TransactionsTDK
)

from .spot import spot_transactions, SpotPaths
from .futures import futures_transactions, FuturesPaths

class ExcelPaths(SpotPaths, FuturesPaths):
  ...

class AutoDetect:
  ...

AUTO_DETECT = AutoDetect()

@dataclass
class Transactions(TransactionsTDK):
  paths: ExcelPaths
  tz: timezone | AutoDetect = AUTO_DETECT
  """Timezone of the files' times."""
  skip_zero_changes: bool = True
  """Skip zero change operations."""

  @property
  def timezone(self) -> timezone:
    if isinstance(self.tz, AutoDetect):
      return datetime.now().astimezone().tzinfo # type: ignore
    else:
      return self.tz
  
  async def transactions(
    self, *, start: datetime | None = None, end: datetime | None = None
  ) -> AsyncIterable[list[Transaction]]:
    for path in self.paths.values():
      if not os.path.exists(path): # type: ignore (yes path is a string, fucking pyright)
        raise FileNotFoundError(f'File not found: {path}')
    for chunk in spot_transactions(self.paths, self.timezone, skip_zero_changes=self.skip_zero_changes):
      yield chunk
    for chunk in futures_transactions(self.paths, self.timezone, skip_zero_changes=self.skip_zero_changes):
      yield chunk