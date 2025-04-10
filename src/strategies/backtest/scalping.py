from backtesting import Strategy


class Scalping(Strategy):
    """
    Trading Strategy 1: Simple scalping based on this video https://www.youtube.com/watch?v=C3bh6Y4LpGs

    Trend detection
    - Uptrend (EMA50>EMA200) - long positions
    - Downtrend - short positions

    Bollinger band edges for entry signals
    - During a uptrend, if price crosses lower bollinger curve, open a long position
    - During a downtrend, if price crosses upper bollinger band, open a short position

    Stop-Loss (SL) = slcoef * ATR
    Take Profit (TP) = TPSL * SL
    """

    # Dummy variables that can be overridden
    tp_pct = None
    sl_pct = None

    def init(self):
        pass

    def next(self):
        curr_close = self.data.Close[-1]
        if (
            all(self.data.EMA_50[-7:] > self.data.EMA_200[-7:])
            and self.data.Close[-1] <= self.data.Lower_Band[-1]
        ):
            sl = curr_close - self.sl_pct * curr_close if self.sl_pct else None
            tp = curr_close + self.tp_pct * curr_close if self.tp_pct else None
            self.buy(sl=sl, tp=tp)
        elif (
            all(self.data.EMA_50[-7:] < self.data.EMA_200[-7:])
            and self.data.Close[-1] >= self.data.Upper_Band[-1]
        ):
            self.position.close()
