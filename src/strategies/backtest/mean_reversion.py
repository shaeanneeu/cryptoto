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

    tp_pct = 0.1
    sl_pct = 0.05

    def init(self):
        self.ma = self.I(ta.sma, self.data.Close.s, length=20)
        self.std = self.I(ta.stdev, self.data.Close.s, length=20)
        self.threshold = 1.5

    def next(self):

        curr_close = price = self.data.Close[-1]
        ma = self.ma[-1]
        std = self.std[-1]

        if not self.position:
            if price < ma - self.threshold * std:
                # self.sell()
                sl = curr_close + self.sl_pct * curr_close
                tp = curr_close - self.tp_pct * curr_close
                self.sell(sl=sl, tp=tp)
            elif price > ma + self.threshold * std:
                # self.buy()
                sl = curr_close - self.sl_pct * curr_close
                tp = curr_close + self.tp_pct * curr_close
                self.buy(sl=sl, tp=tp)
        else:
            if self.position.size > 0 and price >= ma:
                self.position.close()
            elif self.position.size < 0 and price <= ma:
                self.position.close()
