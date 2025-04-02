from typing import Type

import pandas as pd
import pandas_ta as ta
import yfinance as yf

from models.strategy import Strategy


class Asset:
    def __init__(self, ticker: str, start: str, end: str):
        self.ticker = ticker
        self.df = yf.Ticker(ticker).history(start=start, end=end, actions=False)
        self.calculate_technical_indicators()

    def get_data(self) -> pd.DataFrame:
        return self.df

    def calculate_technical_indicators(self):
        df = self.df

        df["EMA_50"] = ta.ema(df["Close"], length=50)
        df["EMA_200"] = ta.ema(df["Close"], length=200)
        df["RSI"] = ta.rsi(df["Close"], length=14)
        df["ATR"] = ta.atr(
            df["High"], df["Low"], df["Close"], length=7
        )  # volatility distance

        bbands = ta.bbands(df["Close"], length=20)
        bbands = bbands.rename(
            columns={
                "BBU_20_2.0": "Upper_Band",
                "BBM_20_2.0": "Middle_Band",
                "BBL_20_2.0": "Lower_Band",
                "BBB_20_2.0": "Band_Width",
                "BBP_20_2.0": "Percent_B",
            }
        )

        stoch = ta.stoch(df["High"], df["Low"], df["Close"])
        stoch = stoch.rename(columns={"STOCHk_14_3_3": "%K", "STOCHd_14_3_3": "%D"})

        macd = ta.macd(df["Close"])
        macd = macd.rename(
            columns={
                "MACD_12_26_9": "MACD",
                "MACDh_12_26_9": "Histogram",
                "MACDs_12_26_9": "Signal",
            }
        )

        df = df.join([bbands, stoch, macd])

        df["OBV"] = ta.obv(df["Close"], df["Volume"])

        self.df = df

    def apply_strategy(self, strategy: Type[Strategy]) -> pd.DataFrame:
        return strategy().generate_signals(self.df)
