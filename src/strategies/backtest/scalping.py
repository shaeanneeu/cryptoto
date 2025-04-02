import pandas_ta as ta
from backtesting import Strategy


class ScalpingFactory:
    @staticmethod
    def get(ema_length=50, ema200_length=200, boll_length=20, boll_std=2, days_continuous_trend=7):
        return Scalping(ema_length, ema200_length, boll_length, boll_std, days_continuous_trend)

class Scalping(Strategy):
    """
    Trading Strategy 1: Simple scalping based on this video https://www.youtube.com/watch?v=C3bh6Y4LpGs

    Trend detection
    - Uptrend (EMA50>EMA200) - long positions
    - Downtrend - short positions

    Bollinger band edges for entry signals
    - During a uptrend, if price crosses lower bollinger curve, open a long position
    - During a downtrend, if price crosses upper bollinger band, open a short position

    Stop-Loss (SL) = slcoef * ATR
    Take Profit (TP) = TPSL * SL
    """

    def init(self, ema_length=50, ema200_length=200, boll_length=20, boll_std=2, days_continuous_trend=7):
        self.ema50 = self.I(ta.ema, self.data.Close.s, length=ema_length)
        self.ema200 = self.I(ta.ema, self.data.Close.s, length=ema200_length)

        def bb_lower(close):
            return ta.bbands(close, length=boll_length, std=boll_std)["BBL_20_2.0"]

        def bb_upper(close):
            return ta.bbands(close, length=boll_length, std=boll_std)["BBU_20_2.0"]

        self.lower_band = self.I(bb_lower, self.data.Close.s)
        self.upper_band = self.I(bb_upper, self.data.Close.s)

        self.days_continuous_trend = days_continuous_trend

    def next(self):
        if (
            all(self.ema50[-self.days_continuous_trend:] > self.ema200[-self.days_continuous_trend:])
            and self.data.Close[-1] <= self.lower_band[-1]
        ):
            self.buy()
        elif (
            all(self.ema50[-self.days_continuous_trend:] < self.ema200[-self.days_continuous_trend:])
            and self.data.Close[-1] >= self.upper_band[-1]
        ):
            self.sell()
