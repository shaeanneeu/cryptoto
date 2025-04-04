import pandas as pd
import pandas_ta as ta

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

        bbands = ta.bbands(df["Close"], length=200)[["BBU_200_2.0", "BBL_200_2.0"]]
        bbands = bbands.rename(
            columns={
                "BBU_200_2.0": "Upper_Band_200",
                "BBL_200_2.0": "Lower_Band_200",
            }
        )

        def total_signal(df: pd.DataFrame, curr):
            pos = df.index.get_loc(curr)

            if df["Close"].iloc[pos] > bbands["Upper_Band_200"].iloc[pos]:
                return LONG
            elif df["Close"].iloc[pos] < bbands["Lower_Band_200"].iloc[pos]:
                return SHORT
            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
