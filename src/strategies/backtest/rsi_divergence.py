import pandas_ta as ta
from backtesting import Strategy


class RSIDivergence(Strategy):
    """
    RSI Divergence Strategy:
    - LONG: Bullish divergence (price lower low, RSI higher low)
    - SHORT: Bearish divergence (price higher high, RSI lower high)
    """

    tp_pct = 0.1
    sl_pct = 0.05

    def init(self):
        self.rsi = ta.rsi(self.data.Close.s, length=14)

    def next(self):
        curr_close = self.data.Close[-1]

        if len(self.data.Close) < 20:
            return

        close = self.data.Close.s
        rsi = self.rsi

        recent_lows = close.iloc[-20:].nsmallest(2).index
        if len(recent_lows) < 2:
            return

        low1, low2 = recent_lows.sort_values()
        if close[low1] > close[low2] and rsi[low1] < rsi[low2]:
            # self.buy()
            sl = curr_close - self.sl_pct * curr_close
            tp = curr_close + self.tp_pct * curr_close
            self.buy(sl=sl, tp=tp)

        recent_highs = close.iloc[-20:].nlargest(2).index
        if len(recent_highs) < 2:
            return

        high1, high2 = recent_highs.sort_values()
        if close[high1] < close[high2] and rsi[high1] > rsi[high2]:
            self.position.close()
