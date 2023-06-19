import talib


class MovingAverageStrategy:
    @staticmethod
    def calculate_moving_averages(candles, period):
        close_prices = [float(candle["close"]) for candle in candles]
        moving_average = talib.SMA(close_prices, timeperiod=period)
        return moving_average

    def check_ma_cross(self, candles):
        ma7 = self.calculate_moving_averages(candles, 7)
        ma25 = self.calculate_moving_averages(candles, 25)
        if ma7[-2] < ma25[-2] and ma7[-1] > ma25[-1]:
            return "Long"
        elif ma7[-2] > ma25[-2] and ma7[-1] < ma25[-1]:
            return "Short"
        else:
            return None
