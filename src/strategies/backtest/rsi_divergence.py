from backtesting import Strategy


class RSIDivergence(Strategy):
    """
    RSI Divergence Strategy:
    - LONG: Bullish divergence (price lower low, RSI higher low)
    - SHORT: Bearish divergence (price higher high, RSI lower high)
    """

    # Dummy variables that can be overridden
    tp_pct = None
    sl_pct = None

    def init(self):
        pass

    def next(self):
        curr_close = self.data.Close[-1]

        if len(self.data.Close) < 20:
            return

        close = self.data.Close.s
        rsi = self.data.RSI.s

        recent_lows = close.iloc[-20:].nsmallest(2, keep="last").index
        if len(recent_lows) < 2:
            return

        low1, low2 = recent_lows.sort_values()
        if close.loc[low1] > close.loc[low2] and rsi.loc[low1] < rsi.loc[low2]:
            sl = curr_close - self.sl_pct * curr_close if self.sl_pct else None
            tp = curr_close + self.tp_pct * curr_close if self.tp_pct else None
            self.buy(sl=sl, tp=tp)

        recent_highs = close.iloc[-20:].nlargest(2).index
        if len(recent_highs) < 2:
            return

        high1, high2 = recent_highs.sort_values()
        if close.loc[high1] < close.loc[high2] and rsi.loc[high1] > rsi.loc[high2]:
            self.position.close()
