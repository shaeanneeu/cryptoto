import pandas_ta as ta
from backtesting import Strategy

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
    def init(self):
        self.mom = self.I(ta.mom, self.data.Close.s, length=10)
    
    def next(self):
        if self.mom[-1] > 0:
            if not self.position:
                self.buy()

        elif self.mom[-1] < 0:
            if self.position:
                self.position.close()
