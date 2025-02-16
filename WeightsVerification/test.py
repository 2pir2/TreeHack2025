import numpy as np

# Define decision tree regression logic
def decision_tree_regression(feature1, feature2):
    """ Simulate a decision tree based on feature splits """
    threshold1 = 15
    threshold2 = 25

    # Fixed leaf node outputs
    output1 = 50  # If feature1 > 15 & feature2 > 25
    output2 = 30  # If feature1 > 15 & feature2 <= 25
    output3 = 20  # If feature1 <= 15 & feature2 > 25
    output4 = 10  # If feature1 <= 15 & feature2 <= 25

    # Decision logic
    if feature1 > threshold1:
        return output1 if feature2 > threshold2 else output2
    else:
        return output3 if feature2 > threshold2 else output4

# Define the Random Forest Regression process
def random_forest_regression(feature_values):
    """ Compute the average prediction from multiple decision trees """
    tree1 = decision_tree_regression(feature_values[0], feature_values[1])
    tree2 = decision_tree_regression(feature_values[0] + 3, feature_values[1])
    tree3 = decision_tree_regression(feature_values[0], feature_values[1] - 2)

    # Compute final prediction as the average of the tree outputs
    prediction = (tree1 + tree2 + tree3) / 3
    return prediction

# Given feature values
feature_values = np.array([20, 30])

# Compute prediction
prediction = random_forest_regression(feature_values)

# Define expected range
min_value = 25
max_value = 55

# Check if prediction is within range
is_valid = min_value <= prediction <= max_value

# Print results
print(f"Feature Values: {feature_values}")
print(f"Prediction: {prediction}")
print(f"Valid Prediction (Within [{min_value}, {max_value}]): {is_valid}")
