import pandas as pd

tickers = ["NVDA", "MSFT"] # TBC
proportions = [0.5, 0.5] # TBC

allocation = pd.DataFrame({"Ticker": tickers, "Proportion": proportions})
# to adjust this file based on max_sharpe_allocation.csv once finalised