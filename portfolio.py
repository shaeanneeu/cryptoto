from typing import List

from asset import Asset


class Portfolio:
    def __init__(self, tickers: List[str], start: str, end: str):
        self.assets = {ticker: Asset(ticker, start, end) for ticker in tickers}
    
    def get_assets(self):
        return self.assets

    def get_asset_information(self, asset):
        if asset in self.assets.keys():
            asset_data = self.assets[asset].df
            return asset_data
        else: 
            return f"Asset {asset} not in portfolio."