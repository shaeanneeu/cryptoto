from backtesting import Strategy
from backtesting.lib import crossover


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

        # def bb_lower(close):
        #     return ta.bbands(close, length=200, std=2)["BBL_200_2.0"]

        # def bb_upper(close):
        #     return ta.bbands(close, length=200, std=2)["BBU_200_2.0"]

        # self.lower_band = self.I(bb_lower, self.data.Close.s)
        # self.upper_band = self.I(bb_upper, self.data.Close.s)

    def next(self):

        curr_close = self.data.Close[-1]

        if not self.position:
            if self.data.Close[-1] > self.data.Upper_Band_200[-1]:
                # self.buy()
                sl = curr_close - self.sl_pct * curr_close
                tp = curr_close + self.tp_pct * curr_close
                self.buy(sl=sl, tp=tp)
            elif self.data.Close[-1] < self.data.Lower_Band_200[-1]:
                # self.sell()
                sl = curr_close + self.sl_pct * curr_close
                tp = curr_close - self.tp_pct * curr_close
                self.sell(sl=sl, tp=tp)
        else:
            if self.position.is_long:
                if crossover(self.data.Upper_Band_200[-1], self.data.Close[-1]):
                    self.position.close()
            elif self.position.is_short:
                if crossover(self.data.Close[-1], self.data.Lower_Band_200[-1]):
                    self.position.close()
