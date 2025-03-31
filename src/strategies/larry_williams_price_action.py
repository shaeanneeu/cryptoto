from backtesting import Strategy


class LarryWilliamsPriceAction(Strategy):
    """
    A price action trading strategy based on
    https://www.youtube.com/watch?v=J6VRMhDnVrM.
    Larry Williams' trading strategy.
    """

    size = 0.1  # Trade size
    sl_pct = 0.02
    tp_pct = 0.04

    def init(self):
        pass

    def next(self):

        curr_close = self.data.Close[-1]

        if (
            self.data.Open[-1] > self.data.Close[-1]
            and self.data.High[-1] > self.data.High[-2]
            and self.data.Low[-1] < self.data.Low[-2]
            and self.data.Close[-1] < self.data.Low[-2]
        ):

            sl = curr_close - self.sl_pct * curr_close
            tp = curr_close + self.tp_pct * curr_close
            self.buy(size=self.size, sl=sl, tp=tp)

        elif (
            self.data.Open[-1] < self.data.Close[-1]
            and self.data.Low[-1] < self.data.Low[-2]
            and self.data.High[-1] > self.data.High[-2]
            and self.data.Close[-1] > self.data.High[-2]
        ):

            sl = curr_close + self.sl_pct * curr_close
            tp = curr_close - self.tp_pct * curr_close
            self.sell(size=self.size, sl=sl, tp=tp)
