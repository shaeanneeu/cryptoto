"""
This script fetches the price history for the NASDAQ Crypto Index and saves it to a CSV file,
using the Tessa API.
"""
import pandas as pd
import tessa
import pendulum
import tqdm

import warnings
import typing


def get_nasdaq_crypto_index() -> list[str]:
    '''
    Get the symbols of the NASDAQ crypto index.
    
    Returns:
        list[str]: The symbols of the NASDAQ crypto index.
    '''
    return [
        'ADA-USD', 'AVAX-USD', 'ETH-USD', 'LINK-USD', 
        'LTC-USD', 'SOL-USD', 'UNI-USD', 'BTC-USD', 'XRP-USD'
    ]

def iter_crypto() -> typing.Iterator[tuple[str, str]]:
    '''
    Iterate over the cryptocurrencies.
    
    Returns:
        typing.Iterator[str]: An iterator over the NASDAQ Crypto Index.
    '''
    
    for symbol in get_nasdaq_crypto_index():
        yield symbol

if __name__ == "__main__":
    # Set the start date to 1st March 2024, for reproducibility
    start_date = "03/01/2024"
    start_date_dt = pd.to_datetime(start_date)
    
    failed_to_fetch = []
    stock_data_list = []
    
    for i, symbol in tqdm.tqdm(enumerate(iter_crypto())):
        try:
            # Get the price history for the symbol
            stock_data, currency = tessa.price_history(symbol)
            stock_data["symbol"] = symbol
            stock_data = stock_data.reset_index()
            
            # Convert the date to a datetime object and filter out dates before the start date
            stock_data["date"] = pd.to_datetime(stock_data["date"]).dt.tz_localize(None)
            stock_data = stock_data[stock_data["date"] > start_date_dt]
            
            # Append the data to the list
            stock_data_list.append(stock_data)
            
        except Exception as e:
            warnings.warn(f"Error getting data for {symbol}: {e}")
            failed_to_fetch.append(symbol)
            
    if failed_to_fetch:
        warnings.warn(
            f"Failed to fetch data for {len(failed_to_fetch)} symbols: {failed_to_fetch}")

    # Concatenate the data
    stock_data_concat = pd.concat(stock_data_list)
    
    # Convert the date to a datetime object
    stock_data_concat["date"] = pd.to_datetime(stock_data_concat["date"], format="%d/%m/%Y")
    stock_data_concat.set_index("date", inplace=True)
    
    # Pivot the data so that each symbol is a column
    stock_data_concat = stock_data_concat.pivot(columns="symbol", values="close").reset_index()

    # Resolve multiple entries for the same date and ticker (take the mean)
    # TODO: Investigate this and see if there is a better way to handle this
    stock_data_concat["date"] = stock_data_concat["date"].dt.normalize()
    data = stock_data_concat.groupby("date").transform(lambda x: x.fillna(x.mean()))
    data["date"] = stock_data_concat["date"]
    data.drop_duplicates(subset="date", inplace=True)
    data = data.reset_index()
    
    # Remove first column (which is the index, not needed)
    data = data.drop(data.columns[0], axis=1)
    
    # Shift date column to the left for readability
    data = data[['date'] + [c for c in data if c != 'date']]
    
    # Save the data to a CSV file
    data.to_csv("data/raw/tessa_nci_prices.csv")
    
    # Calculate the percentage of missing data for each security
    na_percentage = data.isna().mean()*100
    print(f"Percentage of missing data for each security:")
    print(na_percentage[na_percentage > 0])



