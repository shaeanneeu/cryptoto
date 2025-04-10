from backtesting import Strategy


class MACDBollingerBandsMeanReversion(Strategy):
    """
    An indicators + mean reversion trading strategy based on
    https://www.youtube.com/watch?v=qShed6dyrQY.
    Good for prices in range-bound markets.
    """

    # Dummy variables that can be overridden
    tp_pct = None
    sl_pct = None

    def init(self):
        pass

    def next(self):
        if len(self.data.Close) < 2:
            return

        curr_close = self.data.Close[-1]
        prev_close = self.data.Close[-2]

        curr_lower = self.data.Lower_Band_200[-1]
        prev_lower = self.data.Lower_Band_200[-2]
        curr_upper = self.data.Upper_Band_200[-1]
        prev_upper = self.data.Upper_Band_200[-2]

        curr_macd_hist = self.data.Histogram[-1]
        prev_macd_hist = self.data.Histogram[-2]

        if (
            prev_close < curr_close
            and prev_macd_hist < curr_macd_hist
            and prev_close < prev_lower
            and curr_close > curr_lower
        ):
            sl = curr_close - self.sl_pct * curr_close if self.sl_pct else None
            tp = curr_close + self.tp_pct * curr_close if self.tp_pct else None
            self.buy(sl=sl, tp=tp)

        elif (
            prev_close > curr_close
            and prev_macd_hist > curr_macd_hist
            and prev_close > prev_upper
            and curr_close < curr_upper
        ):
            self.position.close()
