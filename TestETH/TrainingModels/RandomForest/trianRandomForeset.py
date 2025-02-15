import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load ETH price data (Only selecting timestamp, open, and close)
csv_filename = r"/Users/hanxu/Desktop/TreeHack/TreeHack2025/ETH.csv"
df = pd.read_csv(csv_filename, usecols=["timestamp", "open", "close"])

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Feature Engineering: Add Moving Averages
df["SMA_10"] = df["close"].rolling(window=10).mean()
df["SMA_50"] = df["close"].rolling(window=50).mean()  # Fixed SMA_50 window

# Drop NaN values from rolling calculations
df = df.dropna().copy()

# Target variable: Predict next close price
df["future_close"] = df["close"].shift(-1)

# Drop NaN values after shifting
df = df.dropna()

# Define features (X) and target (y)
X = df[["open", "close", "SMA_10", "SMA_50"]]
y = df["future_close"]

# Split into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Model for Close Price Prediction
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate Model
mae = mean_absolute_error(y_test, y_pred)

# Save Model
joblib.dump(model, "eth_price_model.pkl")
print("Model saved as eth_price_model.pkl")

# Save Model Performance
performance_data = pd.DataFrame({"Actual_Close": y_test, "Predicted_Close": y_pred})
performance_csv = "eth_price_model_performance.csv"
performance_data.to_csv(performance_csv, index=False)

# Output Mean Absolute Error
print(f"Mean Absolute Error (Close Price): {mae}")
