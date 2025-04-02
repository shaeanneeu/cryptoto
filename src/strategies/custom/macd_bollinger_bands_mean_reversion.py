import pandas as pd
import pandas_ta as ta

from models.signals import HOLD, LONG, SHORT
from models.strategy import Strategy


class MACDBollingerBandsMeanReversion(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """

        An indicators + mean reversion trading strategy based on
        https://www.youtube.com/watch?v=qShed6dyrQY.
        Good for prices in range-bound markets.

        Parameters:
            df (pd.DataFrame): An asset's historical data.

        Returns:
            pd.DataFrame: The input DataFrame with an additional column of trading
            signals.
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
            prev_macd_hist = df["MACD"][pos - 1] - df["Signal"][pos - 1]
            curr_macd_hist = df["MACD"][pos] - df["Signal"][pos]

            if (
                df["Close"][pos - 1] < df["Close"][pos]
                and prev_macd_hist < curr_macd_hist
                and df["Close"][pos - 1] < bbands["Lower_Band_200"][pos - 1]
                and df["Close"][pos] > bbands["Lower_Band_200"][pos]
            ):
                return LONG

            if (
                df["Close"][pos - 1] > df["Close"][pos]
                and prev_macd_hist > curr_macd_hist
                and df["Close"][pos - 1] > bbands["Upper_Band_200"][pos - 1]
                and df["Close"][pos] < bbands["Upper_Band_200"][pos]
            ):
                return SHORT

            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
