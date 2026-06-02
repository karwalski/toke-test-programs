import sys
import csv
import json

def matrix_multiply(A, B):
    """Multiply two matrices"""
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    if cols_A != rows_B:
        raise ValueError("Cannot multiply matrices")
    
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

def transpose(matrix):
    """Transpose a matrix"""
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def matrix_inverse(matrix):
    """Calculate matrix inverse using Gaussian elimination"""
    n = len(matrix)
    # Create augmented matrix [A|I]
    aug = [row[:] + [0]*n for row in matrix]
    for i in range(n):
        aug[i][n+i] = 1
    
    # Forward elimination
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(aug[k][i]) > abs(aug[max_row][i]):
                max_row = k
        aug[i], aug[max_row] = aug[max_row], aug[i]
        
        # Make diagonal element 1
        pivot = aug[i][i]
        for j in range(2*n):
            aug[i][j] /= pivot
        
        # Eliminate column
        for k in range(n):
            if k != i:
                factor = aug[k][i]
                for j in range(2*n):
                    aug[k][j] -= factor * aug[i][j]
    
    # Extract inverse matrix
    return [[aug[i][j] for j in range(n, 2*n)] for i in range(n)]

def linear_regression(X, y):
    """Perform linear regression using normal equation"""
    # Add intercept column
    X_with_intercept = [[1] + row for row in X]
    
    # Calculate (X^T * X)^-1 * X^T * y
    X_T = transpose(X_with_intercept)
    XTX = matrix_multiply(X_T, X_with_intercept)
    XTX_inv = matrix_inverse(XTX)
    XTy = matrix_multiply(X_T, [[yi] for yi in y])
    coeffs = matrix_multiply(XTX_inv, XTy)
    
    # Extract coefficients
    intercept = coeffs[0][0]
    coef = [coeffs[i][0] for i in range(1, len(coeffs))]
    
    # Calculate predictions
    predictions = []
    for i in range(len(X)):
        pred = intercept + sum(coef[j] * X[i][j] for j in range(len(coef)))
        predictions.append(pred)
    
    # Calculate R-squared
    y_mean = sum(y) / len(y)
    ss_tot = sum((yi - y_mean)**2 for yi in y)
    ss_res = sum((y[i] - predictions[i])**2 for i in range(len(y)))
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 1.0
    
    return coef, intercept, r_squared, predictions

# Read CSV data from stdin
input_data = sys.stdin.read().strip()
lines = input_data.split('\n')

# Parse CSV
reader = csv.DictReader(lines)
data = list(reader)

# Extract features and target
feature_cols = [col for col in reader.fieldnames if col != 'yield']
X = [[float(row[col]) for col in feature_cols] for row in data]
y = [float(row['yield']) for row in data]

# Train linear regression model
coefficients, intercept, r_squared, predictions = linear_regression(X, y)

# Round to 2 decimal places for output formatting
coefficients = [round(c, 2) for c in coefficients]
intercept = round(intercept, 2)

# Create output
result = {
    "model_type": "linear",
    "r_squared": r_squared,
    "coefficients": coefficients,
    "intercept": intercept
}

print(json.dumps(result, separators=(',', ':')))