import pandas as pd

from models.signals import HOLD, LONG, SHORT
from models.strategy import Strategy


class VolumeSpikeReversal(Strategy):
    """
    Volume Spike Reversal Strategy:
    - LONG: Volume spike + bullish candle + recent downtrend
    - SHORT: Volume spike + bearish candle + recent uptrend
    Parameters:
        df (pd.DataFrame): Asset's historical OHLCV data.
    Returns:
        pd.DataFrame: DataFrame with 'TotalSignal' column.
    """

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:

        def is_downtrend(close_series):
            return all(close_series[-7:] < close_series[-7:])

        def is_uptrend(close_series):
            return all(close_series[-7:] > close_series[-7:])

        def total_signal(df: pd.DataFrame, curr):
            pos = df.index.get_loc(curr)
            if pos < 11:
                return HOLD

            row = df.iloc[pos]
            prev_closes = df["Close"].iloc[pos - 10 : pos]

            volume_spike = row["Volume"] > 2 * df["SMA_Volume_10"].iloc[pos]

            if volume_spike:
                if row["Close"] > row["Open"] and is_downtrend(prev_closes):
                    return LONG
                elif row["Close"] < row["Open"] and is_uptrend(prev_closes):
                    return SHORT
                # if row["Close"] < row["Open"] and is_uptrend(prev_closes):
                #     return SHORT

            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
