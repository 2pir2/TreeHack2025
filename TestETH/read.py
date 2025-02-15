import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Fetch ETH historical price data from CoinGecko API
url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=14"
response = requests.get(url)
print(response.headers)
if response.status_code == 200:
    data = response.json()

    # Convert API response to DataFrame
    df = pd.DataFrame(data["prices"], columns=["timestamp", "close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    # Fetch open prices (from market data API)
    market_data_url = "https://api.coingecko.com/api/v3/coins/ethereum/ohlc?vs_currency=usd&days=14"
    market_response = requests.get(market_data_url)

    market_data = market_response.json()
        
        # Convert OHLC data to DataFrame
    market_df = pd.DataFrame(market_data, columns=["timestamp", "open", "high", "low", "close"])
    market_df["timestamp"] = pd.to_datetime(market_df["timestamp"], unit="ms")
    

        # Merge open and close prices
    df = df.merge(market_df[["timestamp", "open"]], on="timestamp", how="left")
    market_df.to_csv("eth_price_data.csv",index=False)
        # Drop NaN values
        # df = df.dropna()
        # print(market_df)
        # df.to_csv(r"/Users/hanxu/Desktop/TreeHack/TestETH/out.csv")
    print(market_df)
#         # Feature Engineering: Add Moving Averages
#         df["SMA_10"] = df["close"].rolling(window=10).mean()
#         df["SMA_50"] = df["close"].rolling(window=50).mean()

#         # Target variable: Predict next open and close prices
#         df["future_close"] = df["close"].shift(-1)
#         df["future_open"] = df["open"].shift(-1)

#         # Drop NaN values after shifting
#         df = df.dropna()

#         # Define features (X) and target (y)
#         X = df[["open", "close", "SMA_10", "SMA_50"]]
#         y_close = df["future_close"]
#         y_open = df["future_open"]

#         # Split into training (80%) and testing (20%)
#         X_train, X_test, y_train_close, y_test_close = train_test_split(X, y_close, test_size=0.2, random_state=42)
#         X_train, X_test, y_train_open, y_test_open = train_test_split(X, y_open, test_size=0.2, random_state=42)

#         # Train Random Forest Model for Close Price Prediction
#         model_close = RandomForestRegressor(n_estimators=100, random_state=42)
#         model_close.fit(X_train, y_train_close)

#         # Train Random Forest Model for Open Price Prediction
#         model_open = RandomForestRegressor(n_estimators=100, random_state=42)
#         model_open.fit(X_train, y_train_open)

#         # Make predictions
#         y_pred_close = model_close.predict(X_test)
#         y_pred_open = model_open.predict(X_test)

#         # Evaluate Model
#         mae_close = mean_absolute_error(y_test_close, y_pred_close)
#         mae_open = mean_absolute_error(y_test_open, y_pred_open)

#         # Output Mean Absolute Errors
#         print(f"Mean Absolute Error (Close Price): {mae_close}")
#         print(f"Mean Absolute Error (Open Price): {mae_open}")

#     else:
#         print("Error fetching open prices from CoinGecko API.")

# else:
#     print("Error fetching close prices from CoinGecko API.")
