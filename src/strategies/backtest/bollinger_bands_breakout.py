from backtesting import Strategy


class BollingerBandsBreakout(Strategy):
    """
    An indicators + trend-following trading strategy based on
    https://www.tradingview.com/chart/SP500/fOniByDO-Bollinger-Bands-Basics-and-Breakout-Strategy/
    and https://www.youtube.com/watch?v=FdU3q1wspbk.
    """

    tp_pct = 0.1
    sl_pct = 0.05

    def init(self):
        pass

    def next(self):

        curr_close = self.data.Close[-1]

        if self.data.Close[-1] > self.data.Upper_Band_200[-1]:
            # self.buy()
            sl = curr_close - self.sl_pct * curr_close
            tp = curr_close + self.tp_pct * curr_close
            self.buy(sl=sl, tp=tp)
        elif (
            self.position.is_long and self.data.Upper_Band_200[-1] > self.data.Close[-1]
        ):
            self.position.close()
