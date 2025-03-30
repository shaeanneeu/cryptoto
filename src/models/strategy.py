from abc import ABC, abstractmethod

import pandas as pd


class Strategy(ABC):
    """
    Interface for a trading strategy.
    """

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Given a DataFrame of an asset's historical data, generate trading signals.
        
        Parameters:
            df (pd.DataFrame): An asset's historical data.

        Returns:
            pd.DataFrame: The input DataFrame with an additional column of signals
            indicating hold/short/long decisions.
        """
        pass