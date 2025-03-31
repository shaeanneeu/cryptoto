from backtesting import Strategy

class VolumeSpikeReversal(Strategy):
    """
    Volume Spike Reversal Strategy:
    - LONG: Volume spike + bullish candle + recent downtrend
    - SHORT: Volume spike + bearish candle + recent uptrend
    """
    def init(self):
        pass
    
    def next(self):
        if len(self.data.Close) < 10:
            return
        
        sma10_volume = self.data.Volume[-10:].mean()
        
        if self.data.Volume[-1] <= 2 * sma10_volume:
            return
        
        if self.data.Close[-1] < self.data.Open[-1] \
            and self.data.Close[-2] > self.data.Close[-1]:
            self.sell()
        
        if self.data.Close[-1] > self.data.Open[-1] \
            and self.data.Close[-2] < self.data.Close[-1]:
            self.buy()