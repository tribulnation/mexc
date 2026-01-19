from typing_extensions import TypedDict, Required
from datetime import timezone

from trading_sdk.reporting.transactions import (
  Operation, SinglePostingOperation, Transaction, match_transactions
)

from .util import UniqueIds
from .postings import futures_capital_flow
from .operations import futures_trades

class FuturesPaths(TypedDict, total=False):
  futures_capital_flow: Required[str]
  futures_trades: str

def futures_transactions(
  paths: FuturesPaths, tz: timezone, *,
  skip_zero_changes: bool = True
):
  postings = list(futures_capital_flow.parse(paths['futures_capital_flow'], skip_zero_changes=skip_zero_changes))

  operations: list[Operation] = []
  if (path := paths.get('futures_trades')) is not None:
    operations = list(futures_trades.parse(path, tz, skip_zero_changes=skip_zero_changes))

  matched_txs, other_postings = match_transactions(postings, operations)
  yield from matched_txs

  ids = UniqueIds()
  for p in other_postings:
    id = ids.new(f'{p.type};{p.time:%Y-%m-%d %H:%M:%S}')
    yield Transaction(
      operation=SinglePostingOperation.of(id, p),
      postings=[p]
    )