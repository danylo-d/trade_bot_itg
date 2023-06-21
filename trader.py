import time
import datetime

from api import BinanceAPI
from strategy import MovingAverageStrategy


class TradingBot:
    def __init__(
        self,
        api_key,
        api_secret,
        ticker,
        leverage,
        candles_delay,
        order_size,
        long_tp_perc,
        short_tp_perc,
    ):
        self.api = BinanceAPI(api_key, api_secret)
        self.ticker = ticker
        self.leverage = leverage
        self.candles_delay = candles_delay
        self.order_size = order_size
        self.long_tp_perc = long_tp_perc
        self.short_tp_perc = short_tp_perc
        self.strategy = MovingAverageStrategy()

    def enter_long_position(self, price):
        stop_loss_price = price - (price * 0.02)  # 2% Stop Loss
        take_profit_price = price + (price * self.long_tp_perc)
        return (
            self.api.create_limit_buy_order(
                self.ticker,
                self.order_size,
                price,
                {"stopPrice": stop_loss_price, "type": "STOP_MARKET"},
            ),
            take_profit_price,
        )

    def enter_short_position(self, price):
        stop_loss_price = price + (price * 0.02)  # 2% Stop Loss
        take_profit_price = price - (price * self.short_tp_perc)
        return (
            self.api.create_limit_sell_order(
                self.ticker,
                self.order_size,
                price,
                {"stopPrice": stop_loss_price, "type": "STOP_MARKET"},
            ),
            take_profit_price,
        )

    def process_trades(self):
        print("The robot is running. Waiting for new data...")
        while True:
            try:
                candles = self.api.fetch_candles(
                    self.ticker, timeframe="1m", limit=26 + self.candles_delay
                )
                current_candle = candles[-2]

                position = self.strategy.check_ma_cross(candles)

                if position == "Long":
                    entry_order, take_profit_price = self.enter_long_position(
                        current_candle[4]
                    )
                    print(
                        f"{datetime.datetime.now()}: Entry into the Long position at a price {current_candle[4]}, "
                        f"Take Profit: {take_profit_price}"
                    )

                elif position == "Short":
                    entry_order, take_profit_price = self.enter_short_position(
                        current_candle[4]
                    )
                    print(
                        f"{datetime.datetime.now()}: Entry into the Short position at a price {current_candle[4]}, "
                        f"Take Profit: {take_profit_price}"
                    )

                open_orders = self.api.fetch_open_orders(symbol=self.ticker)
                for order in open_orders:
                    if order["type"] == "STOP_MARKET":
                        if order["side"] == "buy":
                            if current_candle[4] >= take_profit_price:
                                self.api.create_market_sell_order(
                                    self.ticker, order["amount"]
                                )
                                print(
                                    f"{datetime.datetime.now()}: "
                                    f"Long position is closed at the price of {current_candle[4]}"
                                )
                        elif order["side"] == "sell":
                            if current_candle[4] <= take_profit_price:
                                self.api.create_market_buy_order(
                                    self.ticker, order["amount"]
                                )
                                print(
                                    f"{datetime.datetime.now()}: "
                                    f"Short position is closed at the price of {current_candle[4]}"
                                )
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(60)

    def run(self):
        self.process_trades()
