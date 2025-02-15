import ccxt
import pandas as pd
from datetime import datetime, timedelta

# Initialize Binance exchange
exchange = exchange = ccxt.coinbase()

# Define symbol and timeframe
symbol = "ETH/USDT"  # ETH price in USDT
timeframe = "1h"  # 1-hour interval
since = exchange.parse8601((datetime.utcnow() - timedelta(days=7)).isoformat())  # Past week

# Fetch historical OHLCV (Open, High, Low, Close, Volume) data
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since)

# Convert to DataFrame
df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])

# Convert timestamp to human-readable format
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

# Select only necessary columns
df = df[["timestamp", "open", "close"]]

# Print the DataFrame
print(df)  # Show first 10 rows
