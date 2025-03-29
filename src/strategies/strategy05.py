import pandas as pd

from utils.signals import HOLD, LONG, SHORT
from utils.strategy import Strategy


class RSIDivergence(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        RSI Divergence Strategy:
        - LONG: Bullish divergence (price lower low, RSI higher low)
        - SHORT: Bearish divergence (price higher high, RSI lower high)

        Parameters:
            df (pd.DataFrame): Asset's historical data.

        Returns:
            pd.DataFrame: DataFrame with 'TotalSignal' column.
        """

        def compute_rsi(series, period=14):
            delta = series.diff()

            gain = delta.clip(lower=0)
            loss = -delta.clip(upper=0)

            avg_gain = gain.rolling(window=period).mean()
            avg_loss = loss.rolling(window=period).mean()

            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return rsi

        """
        def compute_rsi(series, period=14):
            delta = series.diff()
            gain = np.where(delta > 0, delta, 0)
            loss = np.where(delta < 0, -delta, 0)

            avg_gain = pd.Series(gain).rolling(window=period).mean()
            avg_loss = pd.Series(loss).rolling(window=period).mean()

            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return pd.Series(rsi, index=series.index)'
        """

        df["RSI"] = compute_rsi(df["Close"])

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

            # Get last two local maxima
            recent_highs = close.iloc[pos - 10 : pos].nlargest(2).index
            if len(recent_highs) < 2:
                return HOLD

            high1, high2 = recent_highs.sort_values()
            if close[high1] < close[high2] and rsi[high1] > rsi[high2]:
                return SHORT  # Bearish divergence

            return HOLD

        df["TotalSignal"] = df.apply(lambda row: total_signal(df, row.name), axis=1)

        return df
