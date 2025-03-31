import pandas_ta as ta
from backtesting import Strategy


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

    def init(self):
        self.ema50 = self.I(ta.ema, self.data.Close.s, length=50)
        self.ema200 = self.I(ta.ema, self.data.Close.s, length=200)

        def bb_lower(close):
            return ta.bbands(close, length=20, std=2)["BBL_20_2.0"]

        def bb_upper(close):
            return ta.bbands(close, length=20, std=2)["BBU_20_2.0"]

        self.lower_band = self.I(bb_lower, self.data.Close.s)
        self.upper_band = self.I(bb_upper, self.data.Close.s)

    def next(self):
        if (
            all(self.ema50[-7:] > self.ema200[-7:])
            and self.data.Close[-1] <= self.lower_band[-1]
        ):
            self.buy()
        elif (
            all(self.ema50[-7:] < self.ema200[-7:])
            and self.data.Close[-1] >= self.upper_band[-1]
        ):
            self.sell()
