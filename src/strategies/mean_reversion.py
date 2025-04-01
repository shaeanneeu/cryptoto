import pandas_ta as ta
from backtesting import Strategy

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
    def init(self):
        self.ma = self.I(ta.sma, self.data.Close.s, length=20)
        self.std = self.I(ta.stdev, self.data.Close.s, length=20)
        self.threshold = 1.5

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