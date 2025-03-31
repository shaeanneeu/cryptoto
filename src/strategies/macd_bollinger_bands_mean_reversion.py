import pandas_ta as ta
from backtesting import Strategy


def bbands(data):
    # 200 as per video below
    return ta.bbands(data.Close.s, 200).to_numpy()


def macd(data):
    return ta.macd(data.Close.s).to_numpy()


class MACDBollingerBandsMeanReversion(Strategy):
    """
    An indicators + mean reversion trading strategy based on
    https://www.youtube.com/watch?v=qShed6dyrQY.
    Good for prices in range-bound markets.
    """

    size = 0.1  # Trade size
    sl_pct = 0.02
    tp_pct = 0.04

    def init(self):

        (
            self.lower_band,
            self.middle_band,
            self.upper_band,
            self.band_width,
            self.percent_b,
        ) = self.I(bbands, self.data)

        self.macd, self.macd_histogram, self.macd_signal = self.I(macd, self.data)

    def next(self):

        curr_close = self.data.Close[-1]

        if (
            self.data.Close[-2] < self.data.Close[-1]
            and self.macd_histogram[-2] < self.macd_histogram[-1]
            and self.data.Close[-2] < self.lower_band[-2]
            and self.data.Close[-1] > self.lower_band[-1]
        ):
            sl = curr_close - self.sl_pct * curr_close
            tp = curr_close + self.tp_pct * curr_close
            self.buy(size=self.size, sl=sl, tp=tp)

        elif (
            self.data.Close[-2] > self.data.Close[-1]
            and self.macd_histogram[-2] > self.macd_histogram[-1]
            and self.data.Close[-2] > self.upper_band[-2]
            and self.data.Close[-1] < self.upper_band[-1]
        ):
            sl = curr_close + self.sl_pct * curr_close
            tp = curr_close - self.tp_pct * curr_close
            self.sell(size=self.size, sl=sl, tp=tp)
