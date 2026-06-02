import sys
import csv
import json
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def logistic_regression(X, y, learning_rate=0.01, max_iterations=1000):
    n_samples, n_features = len(X), len(X[0])
    
    # Initialize coefficients and intercept
    coefficients = [0.0] * n_features
    intercept = 0.0
    
    for _ in range(max_iterations):
        # Forward pass
        predictions = []
        for i in range(n_samples):
            z = intercept + sum(coefficients[j] * X[i][j] for j in range(n_features))
            predictions.append(sigmoid(z))
        
        # Calculate gradients
        coef_gradients = [0.0] * n_features
        intercept_gradient = 0.0
        
        for i in range(n_samples):
            error = predictions[i] - y[i]
            intercept_gradient += error
            for j in range(n_features):
                coef_gradients[j] += error * X[i][j]
        
        # Update parameters
        intercept -= learning_rate * intercept_gradient / n_samples
        for j in range(n_features):
            coefficients[j] -= learning_rate * coef_gradients[j] / n_samples
    
    return coefficients, intercept

def predict(X, coefficients, intercept):
    predictions = []
    for i in range(len(X)):
        z = intercept + sum(coefficients[j] * X[i][j] for j in range(len(coefficients)))
        prob = sigmoid(z)
        predictions.append(1 if prob >= 0.5 else 0)
    return predictions

def calculate_accuracy(y_true, y_pred):
    correct = sum(1 for i in range(len(y_true)) if y_true[i] == y_pred[i])
    return correct / len(y_true)

# Read CSV from stdin
input_data = sys.stdin.read().strip()
lines = input_data.split('\n')

# Parse CSV
reader = csv.DictReader(lines)
data = list(reader)

# Extract features and target
feature_columns = [col for col in data[0].keys() if col != 'pass']
X = []
y = []

for row in data:
    features = [float(row[col]) for col in feature_columns]
    X.append(features)
    y.append(int(row['pass']))

# Train logistic regression
coefficients, intercept = logistic_regression(X, y)

# Make predictions and calculate accuracy
predictions = predict(X, coefficients, intercept)
accuracy = calculate_accuracy(y, predictions)

# Round to match expected output format
coefficients = [round(c, 2) for c in coefficients]
intercept = round(intercept, 1)
accuracy = round(accuracy, 1)

# Output JSON
result = {
    "coefficients": coefficients,
    "intercept": intercept,
    "accuracy": accuracy
}

print(json.dumps(result, separators=(',', ':')))