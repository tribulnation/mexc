from typing_extensions import TypedDict, Required, Iterable
from datetime import timezone

from trading_sdk.reporting.types import (
  Transaction, Bonus, Yield, InternalTransfer,
  SinglePostingOperation, Other
)

from .util import Module, PostingMatcher
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
} # type: ignore (dumb pyright)

transaction_types: dict[str, type[SinglePostingOperation]] = {
  'Spot Commission Sharing': Bonus,
  'Spot Referral Commission': Bonus,
  'Spot Flexible Savings Airdrop': Bonus,
  'Spot Flexible Savings Staking': Yield,
  'Spot Futures Earn Airdrop': Yield,
  'Spot Kickstarter Airdrop': Yield,
  'Spot Launchpad - Airdrop': Yield,
  'Spot Launchpool Airdrop': Yield,
}

def spot_transactions(
  paths: SpotPaths, tz: timezone, *,
  skip_zero_changes: bool = True
) -> Iterable[list[Transaction]]:

  postings = list(spot_statement.parse(paths['spot_statement'], skip_zero_changes=skip_zero_changes))
  matcher = PostingMatcher.of(postings)
  used = set[int]()

  for key, module in spot_modules.items():
    if (path := paths.get(key)) is not None:
      chunk: list[Transaction] = []
      for op in module.parse(path, tz, skip_zero_changes=skip_zero_changes):
        if (matches := matcher.match(op.expected_postings, time_mode=module.matching_mode)) is None:
          raise ValueError(f'Could not match the postings for the operation: {op}')
        used.update(matches)
        chunk.append(Transaction(operation=op, postings=[postings[i] for i in matches] + op.fixed_postings))
      yield chunk

  unused = set(range(len(postings))) - used
  others: list[Transaction] = []
  for i in unused:
    p = postings[i]
    if (cls := transaction_types.get(p.tag)) is not None:
      op = cls(time=p.time, asset=p.asset, qty=p.change, tag=p.tag) # type: ignore
    elif p.tag == 'Spot To Fiat Account':
      op = InternalTransfer(
        time=p.time, asset=p.asset, qty=p.change, tag=p.tag,
        from_account='Spot', to_account='Fiat',
      )
    elif p.tag == 'Spot To Futures Account':
      op = InternalTransfer(
        time=p.time, asset=p.asset, qty=p.change, tag=p.tag,
        from_account='Spot', to_account='Futures',
      )
    elif p.tag == 'Spot From Fiat Account':
      op = InternalTransfer(
        time=p.time, asset=p.asset, qty=p.change, tag=p.tag,
        from_account='Fiat', to_account='Spot',
      )
    elif p.tag == 'Spot From Futures Account':
      op = InternalTransfer(
        time=p.time, asset=p.asset, qty=p.change, tag=p.tag,
        from_account='Futures', to_account='Spot',
      )
    else:
      op = Other(tag=p.tag, time=p.time)
    others.append(Transaction(operation=op, postings=[p]))

  yield others
