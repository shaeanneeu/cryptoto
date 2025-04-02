import pandas_ta as ta
from backtesting import Strategy

class MeanReversionFactory:
    @staticmethod
    def get(ma_length=20, std_length=20, threshold=1.5):
        class MeanReversionCustom(MeanReversion):
            def init(self):
                super().init(
                    ma_length=ma_length,
                    std_length=std_length,
                    threshold=threshold
                )
        return MeanReversionCustom

class MeanReversion(Strategy):
    """
       ▄▄▄▄███▄▄▄▄      ▄████████    ▄████████ ███▄▄▄▄           
     ▄██▀▀▀███▀▀▀██▄   ███    ███   ███    ███ ███▀▀▀██▄           __         __
     ███   ███   ███   ███    █▀    ███    ███ ███   ███          /  \.-'''-./  \\
     ███   ███   ███  ▄███▄▄▄       ███    ███ ███   ███          \    -   -    /
     ███   ███   ███ ▀▀███▀▀▀     ▀███████████ ███   ███           |   x   x   | 
     ███   ███   ███   ███    █▄    ███    ███ ███   ███           \  .-'''-.  /
     ███   ███   ███   ███    ███   ███    ███ ███   ███            '-\__Y__/-'
      ▀█   ███   █▀    ██████████   ███    █▀   ▀█   █▀                `---`
                                                                  
       ▄████████    ▄████████  ▄█    █▄     ▄████████    ▄████████    ▄████████  ▄█   ▄██████▄  ███▄▄▄▄   
      ███    ███   ███    ███ ███    ███   ███    ███   ███    ███   ███    ███ ███  ███    ███ ███▀▀▀██▄ 
      ███    ███   ███    █▀  ███    ███   ███    █▀    ███    ███   ███    █▀  ███▌ ███    ███ ███   ███ 
     ▄███▄▄▄▄██▀  ▄███▄▄▄     ███    ███  ▄███▄▄▄      ▄███▄▄▄▄██▀   ███        ███▌ ███    ███ ███   ███ 
    ▀▀███▀▀▀▀▀   ▀▀███▀▀▀     ███    ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   ▀███████████ ███▌ ███    ███ ███   ███ 
    ▀███████████   ███    █▄  ███    ███   ███    █▄  ▀███████████          ███ ███  ███    ███ ███   ███ 
      ███    ███   ███    ███ ███    ███   ███    ███   ███    ███    ▄█    ███ ███  ███    ███ ███   ███ 
      ███    ███   ██████████  ▀██████▀    ██████████   ███    ███  ▄████████▀  █▀    ▀██████▀   ▀█   █▀  
      ███    ███                                        ███    ███                                                                                                                                                                                                                                                     
    """
    def init(self, ma_length=20, std_length=20, threshold=1.5):
        self.ma = self.I(ta.sma, self.data.Close.s, length=ma_length)
        self.std = self.I(ta.stdev, self.data.Close.s, length=std_length)
        self.threshold = threshold

    def next(self):
        price = self.data.Close[-1]
        ma = self.ma[-1]
        std = self.std[-1]
        
        if not self.position:
            if price < ma - self.threshold * std:
                self.sell()
            elif price > ma + self.threshold * std:
                self.buy()
        else:
            if self.position.size > 0 and price >= ma:
                self.position.close()
            elif self.position.size < 0 and price <= ma:
                self.position.close()