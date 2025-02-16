import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load the ETH price data
file_path = "/Users/hanxu/Desktop/TreeHack/TreeHack2025/ETH_filtered.csv"
df = pd.read_csv(file_path)

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Create the target variable (1 if price went up, 0 if price went down)
df["price_up"] = (df["close"] > df["open"]).astype(int)

# Select features and target
X = df[["open"]]  # Using 'open' price as feature
y = df["price_up"]

# Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features (optional but recommended for better performance)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the Logistic Regression model
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# Evaluate model performance
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {accuracy:.2f}")

# Predict on new data (example)
new_open_price = [[1650]]  # Replace with real values
new_open_price_scaled = scaler.transform(new_open_price)
prediction = model.predict(new_open_price_scaled)

print("Prediction (1 = Price Up, 0 = Price Down):", prediction[0])
