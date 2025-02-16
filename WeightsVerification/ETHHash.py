import pickle
import os

# Define the model path
model_path = "/Users/hanxu/Desktop/TreeHack/TreeHack2025/TestETH/TrainingModels/RandomForest/eth_price_model.pkl"

# Ensure the file exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

# Load the model
with open(model_path, "rb") as file:
    model = pickle.load(file)

# Print model type
print("Loaded model type:", type(model))

# Check if it's a RandomForestClassifier
if hasattr(model, "estimators_"):
    print("✅ Model is a valid RandomForestClassifier.")
else:
    raise TypeError("❌ Model is not a RandomForestClassifier. Check the saved file format!")
