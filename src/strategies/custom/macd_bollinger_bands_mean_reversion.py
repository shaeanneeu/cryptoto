import pandas as pd

from models.signals import HOLD, LONG, SHORT
from models.strategy import Strategy


class MACDBollingerBandsMeanReversion(Strategy):
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

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:

        def total_signal(df: pd.DataFrame, curr):
            pos = df.index.get_loc(curr)
            prev_macd_hist = df["MACD"].iloc[pos - 1] - df["Signal"].iloc[pos - 1]
            curr_macd_hist = df["MACD"].iloc[pos] - df["Signal"].iloc[pos]

            if (
                df["Close"].iloc[pos - 1] < df["Close"].iloc[pos]
                and prev_macd_hist < curr_macd_hist
                and df["Close"].iloc[pos - 1] < df["Lower_Band_200"].iloc[pos - 1]
                and df["Close"].iloc[pos] > df["Lower_Band_200"].iloc[pos]
            ):
                return LONG

            if (
                df["Close"].iloc[pos - 1] > df["Close"].iloc[pos]
                and prev_macd_hist > curr_macd_hist
                and df["Close"].iloc[pos - 1] > df["Upper_Band_200"].iloc[pos - 1]
                and df["Close"].iloc[pos] < df["Upper_Band_200"].iloc[pos]
            ):
                return SHORT

            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
