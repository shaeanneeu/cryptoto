import pandas_ta as ta
from backtesting import Strategy

class Momentum(Strategy):
    def init(self):
        self.mom = self.I(ta.mom, self.data.Close.s, length=10)
    
    def next(self):
        if self.mom[-1] > 0:
            if not self.position:
                self.buy()

        elif self.mom[-1] < 0:
            if self.position:
                self.position.close()
