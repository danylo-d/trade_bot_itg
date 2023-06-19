import os
import configparser

from trader import TradingBot

config = configparser.ConfigParser()
config.read("config.ini")

# Parameter configuration
api_key = os.getenv("API_KEY", None)
api_secret = os.getenv("SECRET_API_KEY", None)
ticker = config.get("Parameters", "TICKER")
leverage = int(config.get("Parameters", "LEVERAGE"))
candles_delay = int(config.get("Parameters", "CANDLES_DELAY"))
order_size = float(config.get("Parameters", "ORDER_SIZE"))  # 2% of deposit
long_tp_perc = float(
    config.get("Parameters", "LONG_TP_PERC")
)  # 1% of the entry price of the position
short_tp_perc = float(
    config.get("Parameters", "SHORT_TP_PERC")
)  # 0.4% of the entry price of the position

bot = TradingBot(
    api_key,
    api_secret,
    ticker,
    leverage,
    candles_delay,
    order_size,
    long_tp_perc,
    short_tp_perc,
)
bot.run()
