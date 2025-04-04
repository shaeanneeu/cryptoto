import pandas as pd

from models.signals import HOLD, LONG, SHORT
from models.strategy import Strategy


class RSIDivergence(Strategy):
    """
    RSI Divergence Strategy:
    - LONG: Bullish divergence (price lower low, RSI higher low)
    - SHORT: Bearish divergence (price higher high, RSI lower high)
    Parameters:
        df (pd.DataFrame): Asset's historical data.
    Returns:
        pd.DataFrame: DataFrame with 'TotalSignal' column.
    """

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:

        def total_signal(df: pd.DataFrame, curr):
            pos = df.index.get_loc(curr)
            if pos < 20:
                return HOLD

            # Recent two swing lows and RSIs
            close = df["Close"]
            rsi = df["RSI"]

            # Get last two local minima
            recent_lows = close.iloc[pos - 10 : pos].nsmallest(2).index
            if len(recent_lows) < 2:
                return HOLD

            low1, low2 = recent_lows.sort_values()
            if close[low1] > close[low2] and rsi[low1] < rsi[low2]:
                return LONG  # Bullish divergence

            elif close[low1] < close[low2] and rsi[low1] > rsi[low2]:
                # i.e. sell if we have a long position, since we cannot actually short
                return SHORT

            # # Get last two local maxima
            # recent_highs = close.iloc[pos - 10 : pos].nlargest(2).index
            # if len(recent_highs) < 2:
            #     return HOLD

            # high1, high2 = recent_highs.sort_values()
            # if close[high1] < close[high2] and rsi[high1] > rsi[high2]:
            #     return SHORT  # Bearish divergence

            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
