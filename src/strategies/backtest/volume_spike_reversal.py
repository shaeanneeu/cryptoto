from backtesting import Strategy


class VolumeSpikeReversal(Strategy):
    """
    Volume Spike Reversal Strategy:
    - LONG: Volume spike + bullish candle + recent downtrend
    - SHORT: Volume spike + bearish candle + recent uptrend
    """

    # Dummy variables that can be overridden
    tp_pct = None
    sl_pct = None

    def init(self):
        pass

    def next(self):
        if len(self.data.Close) < 10:
            return

        sma10_volume = self.data.SMA_Volume_10[-1]

        if self.data.Volume[-1] <= 2 * sma10_volume:
            return

        curr_close = self.data.Close[-1]

        if self.data.Close[-1] > self.data.Open[-1] and all(
            self.data.EMA_50[-7:] < self.data.EMA_200[-7:]
        ):
            sl = curr_close - self.sl_pct * curr_close if self.sl_pct else None
            tp = curr_close + self.tp_pct * curr_close if self.tp_pct else None
            self.buy(sl=sl, tp=tp)

        elif self.data.Close[-1] < self.data.Open[-1] and all(
            self.data.EMA_50[-7:] > self.data.EMA_200[-7:]
        ):
            self.position.close()
