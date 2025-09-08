from dataclasses import dataclass
from .my_funding_history import MyFundingHistory
from .my_trades import MyTrades

@dataclass
class UserData(MyFundingHistory, MyTrades):
  ...