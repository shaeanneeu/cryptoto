from typing import List

from utils.asset import Asset


class Portfolio:
    def __init__(self, tickers: List[str], start: str, end: str):
        self.assets = {ticker: Asset(ticker, start, end) for ticker in tickers}
        # TODO: store proportions of assets

    def get_assets(self):
        return self.assets

    def get_asset_data(self, ticker: str):
        if ticker in self.assets.keys():
            asset_data = self.assets[ticker].get_data()
            return asset_data
        else:
            return f"Asset {ticker} not in portfolio."
