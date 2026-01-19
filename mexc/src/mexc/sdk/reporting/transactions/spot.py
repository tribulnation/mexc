from typing_extensions import TypedDict, Required, Iterable
from datetime import timezone

from trading_sdk.reporting.transactions import (
  SinglePostingOperation, Operation,
  Transaction, match_transactions
)
from .util import Module, UniqueIds
from .postings import spot_statement
from .operations import fixed_earn, flexible_earn, deposits, withdrawals, spot_trades, fiat_otc_orders

class SpotPaths(TypedDict, total=False):
  spot_statement: Required[str]
  fixed_earn: str
  flexible_earn: str
  deposits: str
  withdrawals: str
  spot_trades: str
  fiat_otc_orders: str

spot_modules: dict[str, Module] = {
  'fixed_earn': fixed_earn,
  'flexible_earn': flexible_earn,
  'deposits': deposits,
  'withdrawals': withdrawals,
  'spot_trades': spot_trades,
  'fiat_otc_orders': fiat_otc_orders,
}

def spot_transactions(
  paths: SpotPaths, tz: timezone, *,
  skip_zero_changes: bool = True
) -> Iterable[Transaction]:

  postings = list(spot_statement.parse(paths['spot_statement'], skip_zero_changes=skip_zero_changes))

  operations: list[Operation] = []
  for key, module in spot_modules.items():
    if (path := paths.get(key)) is not None:
      operations.extend(module.parse(path, tz, skip_zero_changes=skip_zero_changes))
  
  matched_txs, other_postings = match_transactions(postings, operations)
  yield from matched_txs

  ids = UniqueIds()
  for p in other_postings:
    id = ids.new(f'{p.type};{p.time:%Y-%m-%d %H:%M:%S}')
    yield Transaction(
      operation=SinglePostingOperation.of(id, p),
      postings=[p]
    )