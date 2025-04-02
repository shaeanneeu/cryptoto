import pandas as pd
import pandas_ta as ta

from models.signals import HOLD, LONG, SHORT
from models.strategy import Strategy


class BollingerBandsBreakout(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        An indicators + trend-following trading strategy based on
        https://www.tradingview.com/chart/SP500/fOniByDO-Bollinger-Bands-Basics-and-Breakout-Strategy/
        and https://www.youtube.com/watch?v=FdU3q1wspbk.
        """

        bbands = ta.bbands(df["Close"], length=200)[["BBU_200_2.0", "BBL_200_2.0"]]
        bbands = bbands.rename(
            columns={
                "BBU_200_2.0": "Upper_Band_200",
                "BBL_200_2.0": "Lower_Band_200",
            }
        )

        def total_signal(df: pd.DataFrame, curr):
            pos = df.index.get_loc(curr)

            if df["Close"][pos] > bbands["Upper_Band_200"][pos]:
                return LONG
            elif df["Close"][pos] < bbands["Lower_Band_200"][pos]:
                return SHORT
            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
