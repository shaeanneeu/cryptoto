import pandas as pd
from tessa import price_history, price_point, price_point_strict, price_latest
import pendulum
import ssl
from tqdm import tqdm

securities_failed_to_get = []

# end date is today. Start date is 1 year ago. String format
start_date = (pd.Timestamp.today() - pd.DateOffset(years=1)).strftime("%d/%m/%Y")
historical_data_seperated = []

# Get the historical data for Crpyto
# Top 10 constituents in the S&P Cryptocurrency Broad Digital Market Index 
crpto_names = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "ADA-USD", "TRX-USD", "LTC-USD", "LINK-USD", "AVAX-USD", "LEO-USD"]
for security_name in tqdm(crpto_names):
    crypto_data, currency = price_history(security_name)
    crypto_data["security_name"] = security_name
    crypto_data = crypto_data.reset_index()
    crypto_data["date"] = pd.to_datetime(crypto_data["date"]).dt.tz_localize(None) 
    # get data that has date after start date
    start_date_dt = pd.to_datetime(start_date)
    crypto_data = crypto_data[crypto_data["date"] > start_date_dt]

    historical_data_seperated.append(crypto_data)

# Get the historical data for S&P 500
ssl._create_default_https_context = ssl._create_unverified_context
s_p500_symbols = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]["Symbol"].tolist()
s_p500_stock_names = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]["Security"].tolist()
counter = 1
for symbol,security_name in tqdm(zip(s_p500_symbols,s_p500_stock_names)):
    try:
        stock_data, currency = price_history(symbol)
        stock_data["security_name"] = security_name
        stock_data = stock_data.reset_index()
        stock_data["date"] = pd.to_datetime(stock_data["date"]).dt.tz_localize(None)
        # get data that has date after start date
        start_date_dt = pd.to_datetime(start_date)
        stock_data = stock_data[stock_data["date"] > start_date_dt]

        historical_data_seperated.append(stock_data)
        print(f"Got data for stock #{counter}: {symbol}")
    except Exception as e:
        print(f"Error getting data for {symbol}: {e}")
        securities_failed_to_get.append(symbol)

    counter += 1

# Clean up the data
historical_data = pd.concat(historical_data_seperated)
historical_data["date"] = pd.to_datetime(historical_data["date"], format="%d/%m/%Y")
historical_data.set_index("date", inplace=True)
# Each security_name is a column
historical_data = historical_data.pivot(columns="security_name", values="close").reset_index()
# Cleaning up the issue of multiple timings per day
historical_data["date"] = historical_data["date"].dt.normalize()
data = historical_data.groupby("date").transform(lambda x: x.fillna(x.mean()))
data["date"] = historical_data["date"]
data.drop_duplicates(subset="date", inplace=True)
data = data.reset_index()

# Rearranging columns
# Remove first column
data = data.drop(data.columns[0], axis=1)
# Shift all the columns that end with "USD" to the left
data = data[[c for c in data if c.endswith('USD')] + [c for c in data if not c.endswith('USD')]]
# Shift date column to the left
data = data[['date'] + [c for c in data if c != 'date']]

# Output the data
data.to_csv("historical_pricing_data.csv")

# Other stuff

for s in securities_failed_to_get:
    print("Securities failed to get:")
    print(s)
print(f"Number of failures: {len(securities_failed_to_get)}")

na_percentage = data.isna().mean()*100
print(f"Percentage of missing data for each security:")
print(na_percentage)

# TODO: Investigate the missing data. Might be because weekends and public holidays??? Seems like crypto not affected.
# UPDATE: After adjusting csv, the missing data really looks to be due to weekends/public holidays
