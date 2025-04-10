from backtesting import Strategy


class LarryWilliamsPriceAction(Strategy):
    """
    A price action trading strategy based on
    https://www.youtube.com/watch?v=J6VRMhDnVrM.
    Larry Williams' trading strategy.
    """

    # Dummy variables that can be overridden
    tp_pct = None
    sl_pct = None

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
            sl = curr_close - self.sl_pct * curr_close if self.sl_pct else None
            tp = curr_close + self.tp_pct * curr_close if self.tp_pct else None
            self.buy(sl=sl, tp=tp)

        elif (
            self.data.Open[-1] < self.data.Close[-1]
            and self.data.Low[-1] < self.data.Low[-2]
            and self.data.High[-1] > self.data.High[-2]
            and self.data.Close[-1] > self.data.High[-2]
        ):
            self.position.close()
