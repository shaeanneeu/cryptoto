from typing import List

from utils.asset import Asset


class Portfolio:
    def __init__(self, tickers: List[str], start: str, end: str):
        self.assets = {ticker: Asset(ticker, start, end) for ticker in tickers}
        # TODO: store proportions of assets

    def get_asset(self, ticker: str) -> Asset | str:
        if ticker in self.assets.keys():
            return self.assets[ticker]
        else:
            return f"Asset {ticker} not in portfolio."

    def get_assets(self):
        return self.assets
