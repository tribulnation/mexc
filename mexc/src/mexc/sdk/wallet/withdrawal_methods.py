from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, timedelta

from trading_sdk.types import ApiError
from trading_sdk.wallet.withdrawal_methods import WithdrawalMethod, WithdrawalMethods as WithdrawalMethodsTDK

from mexc.sdk.core import SdkMixin, wrap_exceptions, parse_network

def cacher(ttl: timedelta = timedelta(seconds=10)):
  value = None
  last = None
  async def cached_fn(fn):
    nonlocal value, last
    if last is None or datetime.now() - last > ttl:
      value = await fn()
      last = datetime.now()
    return value

  return cached_fn


currency_info_cached = cacher()

@dataclass
class WithdrawalMethods(WithdrawalMethodsTDK, SdkMixin):
  @wrap_exceptions
  async def withdrawal_methods(self, asset: str):
    match await currency_info_cached(self.client.spot.currency_info):
      case list(currencies):
        for c in currencies:
          if c['coin'] == asset:
            return [
              WithdrawalMethod(
                network=m['netWork'], # type: ignore
                contract_address=m.get('contract'),
                fee=WithdrawalMethod.Fee(
                  asset=asset,
                  amount=Decimal(m['withdrawFee']),
                ),
              )
              for m in c['networkList']
                if m['withdrawEnable']
            ]

        raise ApiError(f'Asset "{asset}" not found')
      case err:
        raise ApiError(err)