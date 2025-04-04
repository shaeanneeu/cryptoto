import pandas as pd

from models.signals import HOLD, LONG, SHORT
from models.strategy import Strategy


class MeanReversion(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:

        threshold = 1.5

        def total_signal(df: pd.DataFrame, curr):

            pos = df.index.get_loc(curr)

            if (
                df["Close"].iloc[pos]
                < df["SMA_20"].iloc[pos] - threshold * df["STD_20"].iloc[pos]
            ):
                return SHORT
            elif (
                df["Close"].iloc[pos]
                > df["SMA_20"].iloc[pos] + threshold * df["STD_20"].iloc[pos]
            ):
                return LONG
            elif (
                df["Close"].iloc[pos] >= df["SMA_20"].iloc[pos]
                or df["Close"].iloc[pos]
                < df["SMA_20"].iloc[pos] - threshold * df["STD_20"].iloc[pos]
            ):
                # i.e. sell if we have a long position, since we cannot actually short
                return SHORT

            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
