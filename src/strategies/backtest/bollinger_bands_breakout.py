from backtesting import Strategy
from backtesting.lib import crossover


class BollingerBandsBreakout(Strategy):
    """
    An indicators + trend-following trading strategy based on
    https://www.tradingview.com/chart/SP500/fOniByDO-Bollinger-Bands-Basics-and-Breakout-Strategy/
    and https://www.youtube.com/watch?v=FdU3q1wspbk.
    """

    # Dummy variables that can be overridden
    tp_pct = None
    sl_pct = None

    def init(self):
        pass

    def next(self):

        curr_close = self.data.Close[-1]

        if not self.position:
            if self.data.Close[-1] > self.data.Upper_Band_200[-1]:
                sl = curr_close - self.sl_pct * curr_close if self.sl_pct else None
                tp = curr_close + self.tp_pct * curr_close if self.tp_pct else None
                self.buy(sl=sl, tp=tp)
            elif self.data.Close[-1] < self.data.Lower_Band_200[-1]:
                self.position.close()
        else:
            if self.position.is_long:
                if crossover(self.data.Upper_Band_200[-1], self.data.Close[-1]):
                    self.position.close()
            elif self.position.is_short:
                if crossover(self.data.Close[-1], self.data.Lower_Band_200[-1]):
                    self.position.close()
