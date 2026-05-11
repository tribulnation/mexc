from dataclasses import dataclass
from .account import Account
from .my_trades import MyTrades
from .orders import Orders

@dataclass
class UserStreams(Account, MyTrades, Orders):
  ...
