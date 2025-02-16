import pandas as pd
import hashlib
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def compute_model_hash(model_path):
    """Computes SHA-256 hash of the saved model file."""
    with open(model_path, "rb") as file:
        model_bytes = file.read()
    return hashlib.sha256(model_bytes).hexdigest()

def randomforest(X_train, y_train, X_test, y_test, model_path="eth_price_model.pkl"):
    """
    Trains a Random Forest model for ETH closing price prediction, saves it, and generates a model hash.
    
    Parameters:
        X_train (DataFrame): Training features
        y_train (Series): Training target (closing price)
        X_test (DataFrame): Testing features
        y_test (Series): Testing target (closing price)
        model_path (str): Path to save the trained model

    Returns:
        str: Hash of the saved model file (for zk-SNARK verification)
    """
    
    # Train Random Forest Model for Close Price Prediction
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate Model
    mae = mean_absolute_error(y_test, y_pred)

    # Save Model
    joblib.dump(model, model_path)
    print(f"✅ Model saved as {model_path}")

    # Compute Model Hash
    model_hash = compute_model_hash(model_path)
    print(f"✅ Model Commitment Hash (SHA-256): {model_hash}")

    # Save Model Performance
    performance_data = pd.DataFrame({"Actual_Close": y_test, "Predicted_Close": y_pred})
    performance_csv = "eth_price_model_performance.csv"
    performance_data.to_csv(performance_csv, index=False)
    print(f"✅ Model performance saved to {performance_csv}")

    # Output Mean Absolute Error
    print(f"📊 RandomForest Mean Absolute Error (Close Price): {mae}")

    return model_hash  # Return the model hash for zk-SNARK verification

# Example Usage
if __name__ == "__main__":
    # Load dataset (Replace with actual dataset path)
    df = pd.read_csv("/Users/hanxu/Desktop/TreeHack/TreeHack2025/ETH.csv")  

    # Feature selection (Assume columns: timestamp, open, close)
    X = df[["timestamp", "open"]]  # Features
    y = df["close"]  # Target (closing price)

    # Convert timestamp to numeric if it's a datetime object
    if pd.api.types.is_datetime64_any_dtype(X["timestamp"]) or isinstance(X["timestamp"].iloc[0], str):
        X["timestamp"] = pd.to_datetime(X["timestamp"]).astype(int) // 10**9  # Convert to Unix time

    # Split dataset into train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model and get hash
    model_commitment_hash = randomforest(X_train, y_train, X_test, y_test)

    # Save hash for zk-SNARK verification
    with open("model_hash.txt", "w") as f:
        f.write(model_commitment_hash)
