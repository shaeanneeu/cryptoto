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
        pass

    def next(self):
        curr_close = self.data.Close[-1]

        if self.data.Momentum[-1] > 0:
            # self.buy()
            sl = curr_close - self.sl_pct * curr_close
            tp = curr_close + self.tp_pct * curr_close
            self.buy(sl=sl, tp=tp)

        # Reverse of entry conditions as exit conditions
        # Position, if any, should always be long, but check anyway
        elif self.position.is_long and self.data.Momentum[-1] < 0:
            self.position.close()
