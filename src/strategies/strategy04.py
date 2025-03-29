import pandas as pd

from utils.signals import HOLD, LONG, SHORT
from utils.strategy import Strategy


class MACDBollingerBandsMeanReversion(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """

        An indicators + mean reversion trading strategy based on
        https://www.youtube.com/watch?v=qShed6dyrQY.
        Good for prices in range-bound markets.

        NOTE: The video uses Bollinger bands with a length of 200.
        Unsure why they choose this length; sticking to the default 20.

        NOTE: The video also has a trend-following strategy that we could try.
        Not implemented yet.

        Parameters:
            df (pd.DataFrame): An asset's historical data.

        Returns:
            pd.DataFrame: The input DataFrame with an additional column of trading
            signals.
        """

        def total_signal(df: pd.DataFrame, curr):

            pos = df.index.get_loc(curr)
            prev_macd_hist = df["MACD"][pos - 1] - df["Signal"][pos - 1]
            curr_macd_hist = df["MACD"][pos] - df["Signal"][pos]

            if (
                df["Close"][pos - 1] < df["Close"][pos]
                and prev_macd_hist < curr_macd_hist
                and df["Close"][pos - 1] < df["Lower_Band"][pos - 1]
                and df["Close"][pos] > df["Lower_Band"][pos]
            ):
                return LONG

            if (
                df["Close"][pos - 1] > df["Close"][pos]
                and prev_macd_hist > curr_macd_hist
                and df["Close"][pos - 1] > df["Upper_Band"][pos - 1]
                and df["Close"][pos] < df["Upper_Band"][pos]
            ):
                return SHORT

            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
