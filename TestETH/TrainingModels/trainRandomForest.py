import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

def randomforest(X_train, y_train, X_test, y_test):
    
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
    print(f"RandomForest Mean Absolute Error (Close Price): {mae}")
