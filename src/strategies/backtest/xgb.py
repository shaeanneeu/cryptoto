from backtesting import Strategy
import xgboost as xgb
import ta
import pandas as pd

'''
Note: This model needs 1 month of data to predict the next day's change.
'''

class XGBFactory:
    @staticmethod
    def get(path_to_model, buy_threshold, close_threshold):
        class XGBCustom(XGB):
            def init(self):
                super().init(
                    path_to_model=path_to_model,
                    buy_threshold=buy_threshold,
                    close_threshold=close_threshold
                )
        return XGBCustom
    

def add_features(prices):
    indicators = ta.add_all_ta_features(prices, open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True)
    indicators['ema2'] = indicators['Close'].ewm(span=2, adjust=False).mean()
    indicators['ema3'] = indicators['Close'].ewm(span=3, adjust=False).mean()
    indicators['ema4'] = indicators['Close'].ewm(span=4, adjust=False).mean()
    indicators['ema5'] = indicators['Close'].ewm(span=5, adjust=False).mean()
    indicators['ema6'] = indicators['Close'].ewm(span=6, adjust=False).mean()
    indicators['ema7'] = indicators['Close'].ewm(span=7, adjust=False).mean()
    indicators['ema10'] = indicators['Close'].ewm(span=10, adjust=False).mean()
    indicators['ema20'] = indicators['Close'].ewm(span=20, adjust=False).mean()
    indicators['ema50'] = indicators['Close'].ewm(span=50, adjust=False).mean()
    indicators['ema100'] = indicators['Close'].ewm(span=100, adjust=False).mean()
    return indicators.copy()


class XGB(Strategy):
    def init(self, path_to_model, buy_threshold, close_threshold):
        self.model = xgb.Booster()
        self.model.load_model(path_to_model)
        self.buy_threshold = buy_threshold
        self.close_threshold = close_threshold
        
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
        
        indicators = add_features(df).iloc[-1:]
        y_pred = self.model.predict(xgb.DMatrix(indicators))[0]
        
        if y_pred > self.buy_threshold:
            self.buy()
        elif y_pred < self.close_threshold:
            self.position.close()