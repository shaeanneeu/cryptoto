from typing import List

from asset import Asset


class Portfolio:
    def __init__(self, tickers: List[str], start: str, end: str):
        self.assets = {ticker: Asset(ticker, start, end) for ticker in tickers}
