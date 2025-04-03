from backtesting import Strategy


class LarryWilliamsPriceAction(Strategy):
    """
    A price action trading strategy based on
    https://www.youtube.com/watch?v=J6VRMhDnVrM.
    Larry Williams' trading strategy.
    """

    tp_pct = 0.1
    sl_pct = 0.05

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
            # self.buy()
            sl = curr_close - self.sl_pct * curr_close
            tp = curr_close + self.tp_pct * curr_close
            self.buy(sl=sl, tp=tp)

        elif (
            self.data.Open[-1] < self.data.Close[-1]
            and self.data.Low[-1] < self.data.Low[-2]
            and self.data.High[-1] > self.data.High[-2]
            and self.data.Close[-1] > self.data.High[-2]
        ):
            # self.sell()
            sl = curr_close + self.sl_pct * curr_close
            tp = curr_close - self.tp_pct * curr_close
            self.sell(sl=sl, tp=tp)
