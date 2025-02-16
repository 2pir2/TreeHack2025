import pandas as pd
from sklearn.model_selection import train_test_split
from TreeHack2025.TestETH.TrainingModels.RandomForest.trainRandomForest import randomforest
from trainxgboost import xgboost

# Load ETH price data (Only selecting timestamp, open, and close)
csv_filename = r"/Users/haipengzhang/Downloads/TreeHack2025/ETH.csv"
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
randomforest(X_train, y_train, X_test, y_test)
xgboost(X_train, y_train, X_test, y_test)
