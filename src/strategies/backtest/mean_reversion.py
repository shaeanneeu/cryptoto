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
        self.threshold = 1.5

    def next(self):

        curr_close = price = self.data.Close[-1]
        sma = self.data.SMA_20[-1]
        std = self.data.STD_20[-1]

        if not self.position:
            if price < sma - self.threshold * std:
                self.position.close()
            elif price > sma + self.threshold * std:
                # self.buy()
                sl = curr_close - self.sl_pct * curr_close
                tp = curr_close + self.tp_pct * curr_close
                self.buy(sl=sl, tp=tp)
        else:
            if self.position.size > 0 and price >= sma:
                self.position.close()
            elif self.position.size < 0 and price <= sma:
                self.position.close()
