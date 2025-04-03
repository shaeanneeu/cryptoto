import pandas_ta as ta
from backtesting import Strategy


class MACDBollingerBandsMeanReversion(Strategy):
    """
    An indicators + mean reversion trading strategy based on
    https://www.youtube.com/watch?v=qShed6dyrQY.
    Good for prices in range-bound markets.
    """

    tp_pct = 0.1
    sl_pct = 0.05

    def init(self):
        self.macd_line, self.macd_hist, self.macd_signal = self.I(
            ta.macd, self.data.Close.s, fast=12, slow=26, signal=9
        )

        # def bb_lower(close):
        #     return ta.bbands(close, length=200, std=2)["BBL_200_2.0"]

        # def bb_upper(close):
        #     return ta.bbands(close, length=200, std=2)["BBU_200_2.0"]

        # self.lower_band = self.I(bb_lower, self.data.Close.s)
        # self.upper_band = self.I(bb_upper, self.data.Close.s)

    def next(self):
        if len(self.data.Close) < 2:
            return

        curr_close = self.data.Close[-1]
        prev_close = self.data.Close[-2]

        curr_lower = self.data.Lower_Band_200[-1]
        prev_lower = self.data.Lower_Band_200[-2]
        curr_upper = self.data.Upper_Band_200[-1]
        prev_upper = self.data.Upper_Band_200[-2]

        curr_macd_hist = self.macd_hist[-1]
        prev_macd_hist = self.macd_hist[-2]

        if (
            prev_close < curr_close
            and prev_macd_hist < curr_macd_hist
            and prev_close < prev_lower
            and curr_close > curr_lower
        ):
            # self.buy()
            sl = curr_close - self.sl_pct * curr_close
            tp = curr_close + self.tp_pct * curr_close
            self.buy(sl=sl, tp=tp)

        elif (
            prev_close > curr_close
            and prev_macd_hist > curr_macd_hist
            and prev_close > prev_upper
            and curr_close < curr_upper
        ):
            self.position.close()
