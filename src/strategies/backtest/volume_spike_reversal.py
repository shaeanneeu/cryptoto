from backtesting import Strategy


class VolumeSpikeReversal(Strategy):
    """
    Volume Spike Reversal Strategy:
    - LONG: Volume spike + bullish candle + recent downtrend
    - SHORT: Volume spike + bearish candle + recent uptrend
    """

    tp_pct = 0.1
    sl_pct = 0.05

    def init(self):
        pass
        # self.ema50 = self.I(ta.ema, self.data.Close.s, length=50)
        # self.ema200 = self.I(ta.ema, self.data.Close.s, length=200)

    def next(self):
        if len(self.data.Close) < 10:
            return

        sma10_volume = self.data.Volume[-10:].mean()

        if self.data.Volume[-1] <= 2 * sma10_volume:
            return

        curr_close = self.data.Close[-1]

        if self.data.Close[-1] > self.data.Open[-1] and all(
            self.data.EMA_50[-7:] < self.data.EMA_200[-7:]
        ):
            # self.buy()
            sl = curr_close - self.sl_pct * curr_close
            tp = curr_close + self.tp_pct * curr_close
            self.buy(sl=sl, tp=tp)

        elif self.data.Close[-1] < self.data.Open[-1] and all(
            self.data.EMA_50[-7:] > self.data.EMA_200[-7:]
        ):
            # self.sell()
            sl = curr_close + self.sl_pct * curr_close
            tp = curr_close - self.tp_pct * curr_close
            self.sell(sl=sl, tp=tp)
