import pandas as pd

from models.signals import HOLD, LONG, SHORT
from models.strategy import Strategy


class Momentum(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:

        def total_signal(df: pd.DataFrame, curr):

            pos = df.index.get_loc(curr)
            if df["Momentum"].iloc[pos] > 0:
                return LONG

            elif df["Momentum"].iloc[pos] < 0:
                return SHORT

            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
