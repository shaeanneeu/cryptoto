import pandas_ta as ta
from backtesting import Strategy

class MomentumFactory:
    @staticmethod
    def get(length=10):
        class MomentumCustom(Momentum):
            def init(self):
                super().init(
                    length=length
                )
        return MomentumCustom

class Momentum(Strategy):
    '''
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
    '''
    def init(self, length=10):
        self.mom = self.I(ta.mom, self.data.Close.s, length=length)
    
    def next(self):
        if self.mom[-1] > 0:
            if not self.position:
                self.buy()

        elif self.mom[-1] < 0:
            if self.position:
                self.position.close()
