from backtesting import Strategy
import xgboost as xgb
import ta
import pandas as pd

'''
Note: This model needs 1 month of data to predict the next day's change.
'''

class XGB(Strategy):
    def init(self, path_to_model):
        self.model = xgb.Booster()
        self.model.load_model(path_to_model)

    def next(self):
        if len(self.data) < 28:
            return
        
        df = pd.DataFrame({
            "Open": self.data.Open.s,
            "High": self.data.High.s,
            "Low": self.data.Low.s,
            "Close": self.data.Close.s,
            "Volume": self.data.Volume.s
        })
        
        results = ta.add_all_ta_features(df, open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True)
        
        print(results)
