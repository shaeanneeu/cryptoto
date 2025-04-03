from backtesting import Strategy


class VolumeSpikeReversal(Strategy):
    """
    Volume Spike Reversal Strategy:
    - LONG: Volume spike + bullish candle + recent downtrend
    - SHORT: Volume spike + bearish candle + recent uptrend
    """

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

        if self.data.Close[-1] > self.data.Open[-1] and all(
            self.data.EMA_50[-7:] < self.data.EMA_200[-7:]
        ):
            self.buy()

        elif self.data.Close[-1] < self.data.Open[-1] and all(
            self.data.EMA_50[-7:] > self.data.EMA_200[-7:]
        ):
            self.sell()
