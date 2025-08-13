from dataclasses import dataclass
from .currency_info import CurrencyInfo
from .deposit_addresses import DepositAddresses
from .withdraw import Withdraw
from .cancel_withdraw import CancelWithdraw
from .deposit_history import DepositHistory
from .withdraw_history import WithdrawHistory

@dataclass
class Wallet(CurrencyInfo, DepositAddresses, Withdraw, CancelWithdraw, DepositHistory, WithdrawHistory):
  ...