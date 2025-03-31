from backtesting import Strategy
import pandas_ta as ta

class MACDBollingerBandsMeanReversion(Strategy):    
    '''
    An indicators + mean reversion trading strategy based on
    https://www.youtube.com/watch?v=qShed6dyrQY.
    Good for prices in range-bound markets.
    '''
    
    size = 0.1  # Trade size
    sl_pct = 0.02
    tp_pct = 0.04
        
    def init(self):
        self.macd_line, self.macd_hist, self.macd_signal = self.I(
            ta.macd, self.data.Close.s, fast=12, slow=26, signal=9
        )

        def bb_lower(close):
            return ta.bbands(close, length=200, std=2)["BBL_200_2.0"]
        
        def bb_upper(close):
            return ta.bbands(close, length=200, std=2)["BBU_200_2.0"]
        
        self.lower_band = self.I(bb_lower, self.data.Close.s)
        self.upper_band = self.I(bb_upper, self.data.Close.s)
    
    def next(self):
        if len(self.data.Close) < 2:
            return
        
        current_close = self.data.Close[-1]
        previous_close = self.data.Close[-2]
        
        current_lower = self.lower_band[-1]
        previous_lower = self.lower_band[-2]
        current_upper = self.upper_band[-1]
        previous_upper = self.upper_band[-2]
        
        current_macd_hist = self.macd_hist[-1]
        previous_macd_hist = self.macd_hist[-2]
        
        if (
            previous_close < current_close and
            previous_macd_hist < current_macd_hist and
            previous_close < previous_lower and
            current_close > current_lower
        ):
            sl = current_close - self.sl_pct * current_close
            tp = current_close + self.tp_pct * current_close
            self.buy(size=self.size, sl=sl, tp=tp)
        
        elif (
            previous_close > current_close and
            previous_macd_hist > current_macd_hist and
            previous_close > previous_upper and
            current_close < current_upper
        ):
            sl = current_close + self.sl_pct * current_close
            tp = current_close - self.tp_pct * current_close
            self.sell(size=self.size, sl=sl, tp=tp)