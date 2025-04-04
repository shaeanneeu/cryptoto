import pandas as pd

from models.signals import HOLD, LONG, SHORT
from models.strategy import Strategy


class BollingerBandsBreakout(Strategy):
    """
    An indicators + trend-following trading strategy based on
    https://www.tradingview.com/chart/SP500/fOniByDO-Bollinger-Bands-Basics-and-Breakout-Strategy/
    and https://www.youtube.com/watch?v=FdU3q1wspbk.

    Parameters:
        df (pd.DataFrame): An asset's historical data.

    Returns:
        pd.DataFrame: The input DataFrame with an additional column of trading
        signals.
    """

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:

        def total_signal(df: pd.DataFrame, curr):
            pos = df.index.get_loc(curr)

            if df["Close"].iloc[pos] > df["Upper_Band_200"].iloc[pos]:
                return LONG
            elif df["Close"].iloc[pos] < df["Upper_Band_200"].iloc[pos]:
                return SHORT

            # elif df["Close"].iloc[pos] < bbands["Lower_Band_200"].iloc[pos]:
            #     return SHORT
            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
