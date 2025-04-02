import pandas as pd

from models.signals import HOLD, LONG, SHORT
from models.strategy import Strategy


class MichaelHarrisPriceAction(Strategy):
    """
    A price action trading strategy based on
    https://www.youtube.com/watch?v=H23GLHD__yY.
    Michael Harris' trading strategy.
    Parameters:
        df (pd.DataFrame): An asset's historical data.
    Returns:
        pd.DataFrame: The input DataFrame with an additional column of trading
        signals.
    """
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:

        def total_signal(df: pd.DataFrame, curr):

            pos = df.index.get_loc(curr)
            high, low = df["High"], df["Low"]

            h, h1, h2, h3 = (
                high.iloc[pos],
                high.iloc[pos - 1],
                high.iloc[pos - 2],
                high.iloc[pos - 3],
            )
            l, l1, l2, l3 = (  # noqa: E741
                low.iloc[pos],
                low.iloc[pos - 1],
                low.iloc[pos - 2],
                low.iloc[pos - 3],
            )

            if (
                h > h1
                and h1 > l
                and l > h2
                and h2 > l1
                and l1 > h3
                and h3 > l2
                and l2 > l3
            ):
                return LONG

            if (
                l < l1
                and l1 < h
                and h < l2
                and l2 < h1
                and h1 < l3
                and l3 < h2
                and h2 < h3
            ):
                return SHORT

            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
