import pandas as pd
import pandas_ta as ta

from models.signals import HOLD, LONG, SHORT
from models.strategy import Strategy


class MeanReversion(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        sma = ta.sma(df["Close"], length=20)
        std = ta.stdev(df["Close"], length=20)
        threshold = 1.5

        def total_signal(df: pd.DataFrame, curr):

            pos = df.index.get_loc(curr)

            if df["Close"].iloc[pos] < sma.iloc[pos] - threshold * std.iloc[pos]:
                return SHORT
            elif df["Close"].iloc[pos] > sma.iloc[pos] + threshold * std.iloc[pos]:
                return LONG

            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
