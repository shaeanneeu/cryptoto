import pandas as pd
import pandas_ta as ta
import yfinance as yf

from tickers import tickers


# Might be useful to eventually wrap these in a custom Strategy as shown here:
# https://github.com/twopirllc/pandas-ta?tab=readme-ov-file#custom
def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df["EMA_50"] = ta.ema(df["Close"], length=50)
    df["EMA_200"] = ta.ema(df["Close"], length=200)

    bbands = ta.bbands(df["Close"], length=20)
    stoch = ta.stoch(df["High"], df["Low"], df["Close"])
    macd = ta.macd(df["Close"])
    df = df.join([bbands, stoch, macd])

    df["OBV"] = ta.obv(df["Close"], df["Volume"])

    return df


for ticker in tickers:
    asset = yf.Ticker(ticker)
    df = asset.history(period="1y", interval="1d", actions=False)
    # Can also use start="yyyy-mm-dd" and end="yyyy-mm-dd" instead of period

    df = calculate_technical_indicators(df)
