import ccxt


class BinanceAPI:
    def __init__(self, api_key, api_secret):
        self.exchange = ccxt.binance(
            {
                "apiKey": api_key,
                "secret": api_secret,
            }
        )

    def get_account_balance(self):
        account_info = self.exchange.fetch_balance()
        return account_info["total"]["USDT"]

    def fetch_candles(self, symbol, timeframe, limit):
        return self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

    def create_limit_buy_order(self, symbol, amount, price, params=None):
        return self.exchange.create_limit_buy_order(
            symbol, amount, price, params=params
        )

    def create_limit_sell_order(self, symbol, amount, price, params=None):
        return self.exchange.create_limit_sell_order(
            symbol, amount, price, params=params
        )

    def create_market_buy_order(self, symbol, amount, params=None):
        return self.exchange.create_market_buy_order(symbol, amount, params=params)

    def create_market_sell_order(self, symbol, amount, params=None):
        return self.exchange.create_market_sell_order(symbol, amount, params=params)

    def fetch_open_orders(self, symbol):
        return self.exchange.fetch_open_orders(symbol=symbol)
