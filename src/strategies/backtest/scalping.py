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

    tp_pct = 0.1
    sl_pct = 0.05

    def init(self):
        pass

    def next(self):
        curr_close = self.data.Close[-1]
        if (
            all(self.data.EMA_50[-7:] > self.data.EMA_200[-7:])
            and self.data.Close[-1] <= self.data.Lower_Band[-1]
        ):
            # self.buy()
            sl = curr_close - self.sl_pct * curr_close
            tp = curr_close + self.tp_pct * curr_close
            self.buy(sl=sl, tp=tp)
        elif (
            all(self.data.EMA_50[-7:] < self.data.EMA_200[-7:])
            and self.data.Close[-1] >= self.data.Upper_Band[-1]
        ):
            self.position.close()
