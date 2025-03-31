import pandas_ta as ta
from backtesting import Strategy
from backtesting.lib import crossover


def bbands(data):
    return ta.bbands(data.Close.s, 200).to_numpy()


class BollingerBandsBreakout(Strategy):
    """
    An indicators + trend-following trading strategy based on
    https://www.fmz.com/strategy/451526 and https://www.youtube.com/watch?v=FdU3q1wspbk.
    """

    size = 0.1  # Trade size
    sl_pct = 0.02
    tp_pct = 0.04

    def init(self):

        (
            self.lower_band,
            self.middle_band,
            self.upper_band,
            self.band_width,
            self.percent_b,
        ) = self.I(bbands, self.data)

    def next(self):

        curr_close = self.data.Close[-1]

        if not self.position:
            if self.data.Close[-1] > self.upper_band[-1]:
                sl = curr_close - self.sl_pct * curr_close
                tp = curr_close + self.tp_pct * curr_close
                self.buy(size=self.size, sl=sl, tp=tp)
            elif self.data.Close[-1] < self.lower_band[-1]:
                sl = curr_close + self.sl_pct * curr_close
                tp = curr_close - self.tp_pct * curr_close
                self.sell(size=self.size, sl=sl, tp=tp)
        else:
            if self.position.is_long:
                if crossover(self.upper_band[-1], self.data.Close[-1]):
                    self.position.close()
            elif self.position.is_short:
                if crossover(self.data.Close[-1], self.lower_band[-1]):
                    self.position.close()
