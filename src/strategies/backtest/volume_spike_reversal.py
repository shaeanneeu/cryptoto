import pandas_ta as ta
from backtesting import Strategy


class VolumeSpikeReversalFactory:
    @staticmethod
    def get(ema_length=50, ema2_length=200, num_of_continuous_trend=7, sma_length=10, volume_threshold=2):
        return VolumeSpikeReversal(ema_length, ema2_length, num_of_continuous_trend, sma_length, volume_threshold)

class VolumeSpikeReversal(Strategy):
    """
    Volume Spike Reversal Strategy:
    - LONG: Volume spike + bullish candle + recent downtrend
    - SHORT: Volume spike + bearish candle + recent uptrend
    """

    def init(self, ema_length=50, ema2_length=200, num_of_continuous_trend=7, sma_length=10, volume_threshold=2):
        self.ema50 = self.I(ta.ema, self.data.Close.s, length=ema_length)
        self.ema200 = self.I(ta.ema, self.data.Close.s, length=ema2_length)
        self.num_of_continuous_trend = num_of_continuous_trend
        self.sma_length = sma_length
        self.volume_threshold = volume_threshold


    def next(self):
        if len(self.data.Close) < self.sma_length:
            return

        sma_volume = self.data.Volume[-self.sma_length:].mean()

        if self.data.Volume[-1] <= self.volume_threshold * sma_volume:
            return

        if self.data.Close[-1] > self.data.Open[-1] and all(
            self.ema50[-self.num_of_continuous_trend:] < self.ema200[-self.num_of_continuous_trend:]
        ):
            self.buy()

        elif self.data.Close[-1] < self.data.Open[-1] and all(
            self.ema50[-self.num_of_continuous_trend:] > self.ema200[-self.num_of_continuous_trend:]
        ):
            self.sell()
