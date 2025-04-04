from backtesting import Strategy


class MichaelHarrisPriceAction(Strategy):
    """
    A price action trading strategy based on
    https://www.youtube.com/watch?v=H23GLHD__yY.
    Michael Harris' trading strategy.
    """

    tp_pct = 0.1
    sl_pct = 0.05

    def init(self):
        pass

    def next(self):
        if len(self.data.Close) < 4:
            return

        curr_close = self.data.Close[-1]

        h, h1, h2, h3 = (
            self.data.High[-1],
            self.data.High[-2],
            self.data.High[-3],
            self.data.High[-4],
        )
        l, l1, l2, l3 = (  # noqa: E741
            self.data.Low[-1],
            self.data.Low[-2],
            self.data.Low[-3],
            self.data.Low[-4],
        )

        # if h > h1 and h1 > l and l > h2 and h2 > l1 and l1 > h3 and h3 > l2 and l2 > l3:
        #     self.position.close()

        if l < l1 and l1 < h and h < l2 and l2 < h1 and h1 < l3 and l3 < h2 and h2 < h3:
            # self.buy()
            sl = curr_close - self.sl_pct * curr_close
            tp = curr_close + self.tp_pct * curr_close
            self.buy(sl=sl, tp=tp)

        # Reverse of entry conditions as exit conditions
        # Position, if any, should always be long, but check anyway
        elif self.position.is_long and (
            l > l1 and l1 > h and h > l2 and l2 > h1 and h1 > l3 and l3 > h2 and h2 > h3
        ):
            self.position.close()
