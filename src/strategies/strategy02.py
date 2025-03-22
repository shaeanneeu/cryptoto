import pandas as pd

from utils.signals import HOLD, LONG, SHORT
from utils.strategy import Strategy


class Strategy02(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """

        A simple price action trading strategy based on
        https://www.youtube.com/watch?v=J6VRMhDnVrM.

        Parameters:
            df (pd.DataFrame): An asset's historical data.

        Returns:
            pd.DataFrame: The input DataFrame with an additional column of trading
            signals.
        """

        def total_signal(df: pd.DataFrame, curr):

            op, high, low, close = df.loc[curr, ["Open", "High", "Low", "Close"]]
            pos = df.index.get_loc(curr)
            prev_high, prev_low = df.iloc[pos - 1][["High", "Low"]]

            if op > close and high > prev_high and low < prev_low and close < prev_low:
                return LONG

            if op < close and low < prev_low and high > prev_high and close > prev_high:
                return SHORT

            return HOLD

        df["TotalSignal"] = df.apply(
            lambda row: total_signal(df, row.name), axis=1
        )

        return df
