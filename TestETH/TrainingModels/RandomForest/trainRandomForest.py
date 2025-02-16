import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

def train_random_forest(X_train, y_train, model_path="eth_price_model.pkl"):
    """
    Trains a Random Forest model for ETH closing price prediction and saves it.

    Parameters:
        X_train (DataFrame): Training features
        y_train (Series): Training target (closing price)
        model_path (str): Path to save the trained model

    Returns:
        model (RandomForestRegressor): Trained Random Forest model
    """
    # Train Random Forest Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save Model
    joblib.dump(model, model_path)

    return model  # Return trained model

# Load dataset
df = pd.read_csv("/Users/hanxu/Desktop/TreeHack/TreeHack2025/ETH.csv")

# Convert timestamp to Unix time
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["timestamp"] = df["timestamp"].astype(int) // 10**9  # Convert to seconds

# Select features and target
X = df[["timestamp", "open"]]  # Features
y = df["close"]  # Target (closing price)

# Identify test set (latest, 1-hour before, 3-hour before, 5-hour before)
test_indices = [-1, -2, -4, -6]  # Last, 1 hour before, 3 hours before, 5 hours before
X_test, y_test = X.iloc[test_indices], y.iloc[test_indices]

# Train on all previous data (excluding the test set)
X_train, y_train = X.drop(X_test.index), y.drop(y_test.index)

# Train model
model = train_random_forest(X_train, y_train)

# Predict closing prices for test timestamps
predicted_close_prices = model.predict(X_test)

# Save predictions to CSV
results_df = pd.DataFrame({
    "Timestamp": X_test["timestamp"].values,
    "Predicted_Close": predicted_close_prices,
    "Actual_Close": y_test.values
})

# Define the CSV filename
csv_filename = r"/Users/hanxu/Desktop/TreeHack/TreeHack2025/TestETH/TrainingModels/RandomForest/eth_price_predictions.csv"

# Save the results to a CSV file
results_df.to_csv(csv_filename, index=False)

# Print message confirming CSV save
print(f"✅ Predictions saved to {csv_filename}")
