import pandas as pd

from utils.signals import HOLD, LONG, SHORT
from utils.strategy import Strategy


class Scalping(Strategy):
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """

        Trading Strategy 1: Simple scalping based on this video https://www.youtube.com/watch?v=C3bh6Y4LpGs

        Trend detection
        - Uptrend (EMA50>EMA200) - long positions
        - Downtrend - short positions
        
        Bollinger band edges for entry signals
        - During a uptrend, if price crosses lower bollinger curve, open a long position 
        - During a downtrend, if price crosses upper bollinger band, open a short position 
        
        Stop-Loss (SL) = slcoef * ATR
        Take Profit (TP) = TPSL * SL 

        Parameters:
            df (pd.DataFrame): An asset's historical data.

        Returns:
            pd.DataFrame: The input DataFrame with an additional column of trading
            signals.
        """
        df.reset_index(inplace=True)

        def ema_signal(df, current_candle, backcandles):
            df_slice = df.reset_index().copy()
            # Get the range of candles to consider - test for multiple backcandles (e.g. 1 week) to prevent fitting to noise
            start = max(0, current_candle - backcandles) 
            end = current_candle
            relevant_rows = df_slice.iloc[start:end]

            # Check if all EMA_fast values are below EMA_slow values
            if all(relevant_rows["EMA_50"] < relevant_rows["EMA_200"]):
                return 1
            elif all(relevant_rows["EMA_50"] > relevant_rows["EMA_200"]):
                return 2
            else:
                return 0

        df['EMASignal'] = df.apply(lambda row: ema_signal(df, row.name, 7) , axis=1)

        def total_signal(df, current_candle, backcandles):
            if (ema_signal(df, current_candle, backcandles)==2
                and df.Close[current_candle]<=df['Lower_Band'][current_candle]
                #and df.RSI[current_candle]<60
                ):
                    return LONG
            
            if (ema_signal(df, current_candle, backcandles)==1
                and df.Close[current_candle]>=df['Upper_Band'][current_candle]
                #and df.RSI[current_candle]>40
                ):
                    
                    return SHORT
            return HOLD

        df['TotalSignal'] = df.apply(lambda row: total_signal(df, row.name, 7), axis=1)

        return df