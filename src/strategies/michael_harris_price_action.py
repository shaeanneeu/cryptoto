from backtesting import Strategy

class MichaelHarrisPriceAction(Strategy):    
    '''
    A price action trading strategy based on
    https://www.youtube.com/watch?v=H23GLHD__yY.
    Michael Harris' trading strategy.
    '''
        
    def init(self):
        pass
    
    def next(self):
        if len(self.data.Close) < 4:
            return
        
        h, h1, h2, h3 = (
            self.data.High[-1],
            self.data.High[-2],
            self.data.High[-3],
            self.data.High[-4],
        )
        l, l1, l2, l3 = (
            self.data.Low[-1],
            self.data.Low[-2],
            self.data.Low[-3],
            self.data.Low[-4],
        )

        if (
            h > h1
            and h1 > l
            and l > h2
            and h2 > l1
            and l1 > h3
            and h3 > l2
            and l2 > l3
        ):
            self.sell()

        if (
            l < l1
            and l1 < h
            and h < l2
            and l2 < h1
            and h1 < l3
            and l3 < h2
            and h2 < h3
        ):
            self.buy()
