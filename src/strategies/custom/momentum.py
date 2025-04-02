import pandas as pd
import pandas_ta as ta

from models.signals import HOLD, LONG, SHORT
from models.strategy import Strategy


class Momentum(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:

        mom = ta.mom(self["Close"], length=10)

        def total_signal(df: pd.DataFrame, curr):

            pos = df.index.get_loc(curr)
            if mom[pos] > 0:
                return LONG

            elif mom[pos] < 0:
                return SHORT

            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
