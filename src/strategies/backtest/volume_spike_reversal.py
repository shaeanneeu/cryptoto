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
            # self.buy()
            sl = curr_close - self.sl_pct * curr_close
            tp = curr_close + self.tp_pct * curr_close
            self.buy(sl=sl, tp=tp)

        # Reverse of entry conditions as exit conditions
        # Position, if any, should always be long, but check anyway
        elif (
            self.position.is_long
            and self.data.Close[-1] < self.data.Open[-1]
            and all(self.data.EMA_50[-7:] > self.data.EMA_200[-7:])
        ):
            self.position.close()
