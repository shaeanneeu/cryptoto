from backtesting import Strategy

class LarryWilliamsPriceAction(Strategy):
    """
    A price action trading strategy based on
    https://www.youtube.com/watch?v=J6VRMhDnVrM.
    Larry Williams' trading strategy.
    """

    def init(self):
        pass

    def next(self):

        if self.data.Open[-1] > self.data.Close \
            and self.data.High[-1] > self.data.High[-2] \
            and self.data.Low[-1] < self.data.Low[-2] \
            and self.data.Close[-1] < self.data.Low[-2]:
            self.buy()
    
        elif self.data.Open[-1] < self.data.Close \
            and self.data.Low[-1] < self.data.Low[-2] \
            and self.data.High[-1] > self.data.High[-2] \
            and self.data.Close[-1] > self.data.High[-2]:
            self.sell()