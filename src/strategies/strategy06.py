import pandas as pd

from utils.signals import HOLD, LONG, SHORT
from utils.strategy import Strategy


class Strategy06(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Volume Spike Reversal Strategy:
        - LONG: Volume spike + bullish candle + recent downtrend
        - SHORT: Volume spike + bearish candle + recent uptrend

        Parameters:
            df (pd.DataFrame): Asset's historical OHLCV data.

        Returns:
            pd.DataFrame: DataFrame with 'TotalSignal' column.
        """

        df["AvgVolume10"] = df["Volume"].rolling(window=10).mean()

        def is_downtrend(close_series):
            return close_series[-1] < close_series[0]

        def is_uptrend(close_series):
            return close_series[-1] > close_series[0]

        def total_signal(df: pd.DataFrame, curr):
            pos = df.index.get_loc(curr)
            if pos < 11:
                return HOLD

            row = df.iloc[pos]
            prev_closes = df["Close"].iloc[pos - 10:pos]

            volume_spike = row["Volume"] > 2 * df["AvgVolume10"].iloc[pos]

            if volume_spike:
                if row["Close"] > row["Open"] and is_downtrend(prev_closes):
                    return LONG
                if row["Close"] < row["Open"] and is_uptrend(prev_closes):
                    return SHORT

            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
