import pandas_ta as ta
from backtesting import Strategy


class Momentum(Strategy):
    """
            __  ___                           __
           /  |/  /___  ____ ___  ___  ____  / /___  ______ ___
          / /|_/ / __ \/ __ `__ \/ _ \/ __ \/ __/ / / / __ `__  |
         / /  / / /_/ / / / / / /  __/ / / / /_/ /_/ / / / / / /
        /_/  /_/\____/_/ /_/ /_/\___/_/ /_/\__/\__,_/_/ /_/ /_/

            ..::::..:.::::::::::::::::::::::::::.::::::..
            .:::::::::::::::::::::::::::::::::::::::::::::::::.
        .::.        .      :      .      .        .          .::.
        .::.        .      :      .      .        .          .::.
        .::.        .      :      .      .         .         .::.
        .::.        .      :      .      .         .         .::.
        .::.        .      :      .      .          .        .::.
        .::.        .      :      .      .          .        .::.
        .::.        .      :      .      .           .       .::.
        .::.        .      :      .      :          *##%+    .::.
        .::.     :#*#%# .**#%#..#*#%%: **###:      *#%%%%%    ::.
        .::.     ##%%%%%##%%%%%##%%%%%#*%%%%%      ##%%%%@    ::.
        .::.     ##%%%%#*%###%#+%%%%%@=%#%%%@       +%%@+    .::.
        .::.      :%@#.  :#%%:  .#%%:  .#%%-                 .::.
        .::.                                                 .::.
       ..:::.....                                         .....:::....
    .--::::-----===.                                    :----:-----===:
    ---------------:                                    :--------------
    """

    tp_pct = 0.1
    sl_pct = 0.05

    def init(self):
        self.mom = self.I(ta.mom, self.data.Close.s, length=10)

    def next(self):
        curr_close = self.data.Close[-1]

        if self.mom[-1] > 0:
            if not self.position:
                # self.buy()
                sl = curr_close - self.sl_pct * curr_close
                tp = curr_close + self.tp_pct * curr_close
                self.buy(sl=sl, tp=tp)

        elif self.mom[-1] < 0:
            if self.position:
                self.position.close()
