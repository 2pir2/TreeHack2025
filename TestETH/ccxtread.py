import ccxt
import pandas as pd
from datetime import datetime, timedelta

# def data_retrieval(start_date, end_date):
#     # Initialize Binance exchange
#     exchange = ccxt.coinbase()

#     # Define symbol and timeframe
#     symbol = "ETH/USDT"  # ETH price in USDT
#     timeframe = "1h"  # 1-hour interval

# # Define the start and end date (Modify these)
# start_date = "2023-09-20"
# end_date = "2023-10-01"

# # Convert to UNIX timestamps
# since = exchange.parse8601(start_date + "T00:00:00Z")  # Start from Sep 20
# until = exchange.parse8601(end_date + "T23:59:59Z")  # End on Oct 1

# # Fetch OHLCV data
# ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since)

# # Convert to DataFrame
# df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])

# # Convert timestamp to human-readable format
# df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

# # **Filter Data Between the Specified Date Range**
# df = df[(df["timestamp"] >= start_date) & (df["timestamp"] <= end_date)]

# # Select only necessary columns
# df = df[["timestamp", "open", "close"]]

# # Print the filtered DataFrame
# print(df.head())

# # Save to CSV
# df.to_csv("ETH_filtered.csv", index=False)

def data_retrieval_price(start_date, end_date, time):
    # Initialize Binance exchange
    exchange = ccxt.coinbase()

    # Define symbol and timeframe
    symbol = "ETH/USDT"  # ETH price in USDT
    timeframe = "1h"  # 1-hour interval

    # Convert to UNIX timestamps
    since = exchange.parse8601(start_date + "T00:00:00Z")  # Start from start of day

    # Fetch OHLCV data
    until = exchange.parse8601(end_date + "T23:59:59Z")  # End at the end of day
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since)

    # Convert to DataFrame
    df = pd.DataFrame(
        ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )

    # Convert timestamp to human-readable format
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    # **Filter Data Between the Specified Date Range**
    df = df[(df["timestamp"] >= start_date) & (df["timestamp"] <= end_date + " " +time)]

    # Select only necessary columns
    df = df[["timestamp", "open", "close"]]
    print(f"@@@ Data retrieval of price data completed from {start_date} to {end_date} @@@")
    return df
