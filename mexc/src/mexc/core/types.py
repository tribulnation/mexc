from typing_extensions import Literal

OrderSide = Literal['BUY', 'SELL']
OrderType = Literal['LIMIT', 'MARKET', 'LIMIT_MAKER', 'IMMEDIATE_OR_CANCEL', 'FILL_OR_KILL']
OrderStatus = Literal['NEW', 'FILLED', 'PARTIALLY_FILLED', 'CANCELED', 'PARTIALLY_CANCELED']
TimeInForce = Literal['GTC', 'IOC', 'FOK']