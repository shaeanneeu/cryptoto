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

    # Dummy variables that can be overridden
    tp_pct = None
    sl_pct = None

    def init(self):
        pass

    def next(self):
        curr_close = self.data.Close[-1]

        if self.data.Momentum[-1] > 0:
            if not self.position:
                sl = curr_close - self.sl_pct * curr_close if self.sl_pct else None
                tp = curr_close + self.tp_pct * curr_close if self.tp_pct else None
                self.buy(sl=sl, tp=tp)

        elif self.data.Momentum[-1] < 0:
            if self.position:
                self.position.close()
