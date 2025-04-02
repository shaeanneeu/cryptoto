from backtesting import Strategy
import pandas_ta as ta

class RSIDivergenceFactory:
    @staticmethod
    def get(rsi_length=14, divergence_length=20):
        return RSIDivergence(rsi_length, divergence_length)

class RSIDivergence(Strategy):
    '''
    RSI Divergence Strategy:
    - LONG: Bullish divergence (price lower low, RSI higher low)
    - SHORT: Bearish divergence (price higher high, RSI lower high)
    '''
        
    def init(self, rsi_length=14, divergence_length=20):
        self.rsi = ta.rsi(self.data.Close.s, length=rsi_length)
        self.divergence_length = divergence_length
    
    def next(self):
        if len(self.data.Close) < self.divergence_length:
            return
        
        close = self.data.Close.s
        rsi = self.rsi

        recent_lows = close.iloc[-self.divergence_length:].nsmallest(2).index
        if len(recent_lows) < 2:
            return
        
        low1, low2 = recent_lows.sort_values()
        if close[low1] > close[low2] and rsi[low1] < rsi[low2]:
            self.sell()
        
        recent_highs = close.iloc[-self.divergence_length:].nlargest(2).index
        if len(recent_highs) < 2:
            return
        
        high1, high2 = recent_highs.sort_values()
        if close[high1] < close[high2] and rsi[high1] > rsi[high2]:
            self.buy()
