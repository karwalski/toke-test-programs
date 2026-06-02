import sys
import csv
import json
from io import StringIO

def read_csv_from_stdin():
    data = []
    reader = csv.DictReader(sys.stdin)
    for row in reader:
        data.append(row)
    return data

def solve_mixture_experiment(data):
    # Extract component names (all columns except the last one which is response)
    headers = list(data[0].keys())
    response_col = headers[-1]
    component_cols = headers[:-1]
    
    # Convert data to numbers
    observations = []
    responses = []
    
    for row in data:
        obs = [float(row[col]) for col in component_cols]
        resp = float(row[response_col])
        observations.append(obs)
        responses.append(resp)
    
    # For mixture experiments, we use a linear model without intercept
    # since components sum to 1: y = β₁x₁ + β₂x₂ + β₃x₃
    # This is a constrained regression problem
    
    # Set up the system of equations: X * β = y
    # where X is the design matrix (observations) and y is responses
    n_obs = len(observations)
    n_components = len(component_cols)
    
    # Use least squares to solve for coefficients
    # Normal equation: (X'X)β = X'y
    
    X = observations
    y = responses
    
    # Calculate X'X
    XtX = [[0.0 for _ in range(n_components)] for _ in range(n_components)]
    for i in range(n_components):
        for j in range(n_components):
            for k in range(n_obs):
                XtX[i][j] += X[k][i] * X[k][j]
    
    # Calculate X'y
    Xty = [0.0 for _ in range(n_components)]
    for i in range(n_components):
        for k in range(n_obs):
            Xty[i] += X[k][i] * y[k]
    
    # Solve the system using Gaussian elimination
    # Since we have the constraint that coefficients should sum appropriately
    # for mixture designs, we'll use a direct approach
    
    # For a simple linear mixture model, solve using matrix operations
    coefficients = solve_linear_system(XtX, Xty)
    
    # Find optimal mixture (maximum predicted response)
    # Since it's linear, optimum is at one of the pure components
    max_coeff = max(coefficients)
    optimal_idx = coefficients.index(max_coeff)
    
    optimal_mixture = [0.0] * n_components
    optimal_mixture[optimal_idx] = 1.0
    
    # Create result
    result = {
        "model": "linear",
        "coefficients": {component_cols[i]: coefficients[i] for i in range(n_components)},
        "optimal_mixture": {component_cols[i]: optimal_mixture[i] for i in range(n_components)}
    }
    
    return result

def solve_linear_system(A, b):
    n = len(b)
    # Gaussian elimination with partial pivoting
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        
        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Make all rows below this one 0 in current column
        for k in range(i + 1, n):
            if A[i][i] != 0:
                c = A[k][i] / A[i][i]
                for j in range(i, n):
                    A[k][j] -= c * A[i][j]
                b[k] -= c * b[i]
    
    # Back substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]
        if A[i][i] != 0:
            x[i] /= A[i][i]
    
    return x

def main():
    data = read_csv_from_stdin()
    result = solve_mixture_experiment(data)
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()