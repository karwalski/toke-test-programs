import sys
import json
from itertools import combinations

def read_csv_from_stdin():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    return lines

def parse_csv(lines):
    # First line contains the include_interactions flag
    include_interactions = lines[0].split(',')[1].lower() == 'true'
    
    # Second line contains headers
    headers = lines[1].split(',')
    
    # Remaining lines contain data
    data = []
    for line in lines[2:]:
        row = [float(x) for x in line.split(',')]
        data.append(row)
    
    return headers, data, include_interactions

def create_design_matrix(headers, data, include_interactions):
    # Separate features from response
    feature_headers = headers[:-1]  # All columns except the last one
    response_header = headers[-1]   # Last column is the response
    
    n_samples = len(data)
    
    # Extract feature values and response values
    X_basic = []
    y = []
    
    for row in data:
        X_basic.append(row[:-1])  # All values except the last one
        y.append(row[-1])         # Last value is the response
    
    # Build feature names and design matrix
    feature_names = feature_headers.copy()
    X = [row[:] for row in X_basic]  # Copy basic features
    
    # Add interaction terms if requested
    if include_interactions:
        for i in range(len(feature_headers)):
            for j in range(i + 1, len(feature_headers)):
                interaction_name = f"{feature_headers[i]}:{feature_headers[j]}"
                feature_names.append(interaction_name)
                
                # Add interaction values for each sample
                for k in range(n_samples):
                    interaction_value = X_basic[k][i] * X_basic[k][j]
                    X[k].append(interaction_value)
    
    return feature_names, X, y

def solve_linear_regression(X, y):
    # Convert to matrix form and solve using normal equations
    # X should be n_samples x n_features
    # y should be n_samples x 1
    
    n_samples = len(X)
    n_features = len(X[0])
    
    # Create X transpose
    X_T = [[X[i][j] for i in range(n_samples)] for j in range(n_features)]
    
    # Compute X_T * X
    XTX = [[0.0 for _ in range(n_features)] for _ in range(n_features)]
    for i in range(n_features):
        for j in range(n_features):
            for k in range(n_samples):
                XTX[i][j] += X_T[i][k] * X_T[j][k]
    
    # Compute X_T * y
    XTy = [0.0 for _ in range(n_features)]
    for i in range(n_features):
        for k in range(n_samples):
            XTy[i] += X_T[i][k] * y[k]
    
    # Solve XTX * beta = XTy using Gaussian elimination
    # Augment the matrix
    augmented = [XTX[i][:] + [XTy[i]] for i in range(n_features)]
    
    # Forward elimination
    for i in range(n_features):
        # Find pivot
        max_row = i
        for k in range(i + 1, n_features):
            if abs(augmented[k][i]) > abs(augmented[max_row][i]):
                max_row = k
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        
        # Make all rows below this one 0 in current column
        for k in range(i + 1, n_features):
            if augmented[i][i] != 0:
                factor = augmented[k][i] / augmented[i][i]
                for j in range(i, n_features + 1):
                    augmented[k][j] -= factor * augmented[i][j]
    
    # Back substitution
    beta = [0.0 for _ in range(n_features)]
    for i in range(n_features - 1, -1, -1):
        beta[i] = augmented[i][n_features]
        for j in range(i + 1, n_features):
            beta[i] -= augmented[i][j] * beta[j]
        if augmented[i][i] != 0:
            beta[i] /= augmented[i][i]
    
    return beta

def calculate_r_squared(X, y, coefficients):
    n_samples = len(y)
    
    # Calculate predictions
    y_pred = []
    for i in range(n_samples):
        pred = sum(X[i][j] * coefficients[j] for j in range(len(coefficients)))
        y_pred.append(pred)
    
    # Calculate mean of y
    y_mean = sum(y) / len(y)
    
    # Calculate total sum of squares
    tss = sum((y[i] - y_mean) ** 2 for i in range(n_samples))
    
    # Calculate residual sum of squares
    rss = sum((y[i] - y_pred[i]) ** 2 for i in range(n_samples))
    
    # Calculate R-squared
    if tss == 0:
        return 1.0
    r_squared = 1 - (rss / tss)
    
    return r_squared

def main():
    lines = read_csv_from_stdin()
    headers, data, include_interactions = parse_csv(lines)
    feature_names, X, y = create_design_matrix(headers, data, include_interactions)
    
    coefficients = solve_linear_regression(X, y)
    r_squared = calculate_r_squared(X, y, coefficients)
    
    # Format output
    coeff_dict = {}
    for i, name in enumerate(feature_names):
        coeff_dict[name] = coefficients[i]
    
    result = {
        "coefficients": coeff_dict,
        "intercept": 0.0,
        "r_squared": r_squared
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()