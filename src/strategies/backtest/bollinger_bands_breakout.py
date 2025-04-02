import pandas_ta as ta
from backtesting import Strategy
from backtesting.lib import crossover

class BollingerBandsBreakoutFactory:
    @staticmethod
    def get(bb_length=200, bb_std=2):
        return BollingerBandsBreakout(bb_length, bb_std)

class BollingerBandsBreakout(Strategy):
    """
    An indicators + trend-following trading strategy based on
    https://www.tradingview.com/chart/SP500/fOniByDO-Bollinger-Bands-Basics-and-Breakout-Strategy/
    and https://www.youtube.com/watch?v=FdU3q1wspbk.
    """

    def init(self, bb_length=200, bb_std=2):
        self.bb_length = bb_length
        self.bb_std = bb_std

        def bb_lower(close):
            return ta.bbands(close, length=self.bb_length, std=self.bb_std)["BBL_200_2.0"]

        def bb_upper(close):
            return ta.bbands(close, length=self.bb_length, std=self.bb_std)["BBU_200_2.0"]

        self.lower_band = self.I(bb_lower, self.data.Close.s)
        self.upper_band = self.I(bb_upper, self.data.Close.s)

    def next(self):

        if not self.position:
            if self.data.Close[-1] > self.upper_band[-1]:
                self.buy()
            elif self.data.Close[-1] < self.lower_band[-1]:
                self.sell()
        else:
            if self.position.is_long:
                if crossover(self.upper_band[-1], self.data.Close[-1]):
                    self.position.close()
            elif self.position.is_short:
                if crossover(self.data.Close[-1], self.lower_band[-1]):
                    self.position.close()
