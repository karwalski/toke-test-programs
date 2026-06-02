import sys
import json
import csv
from io import StringIO

def solve_polynomial_regression():
    lines = sys.stdin.read().strip().split('\n')
    degree = int(lines[0])
    
    # Parse CSV data
    csv_data = '\n'.join(lines[1:])
    reader = csv.DictReader(StringIO(csv_data))
    
    x_values = []
    y_values = []
    
    for row in reader:
        x_values.append(float(row['x']))
        y_values.append(float(row['y']))
    
    n = len(x_values)
    
    # Create Vandermonde matrix for polynomial fitting
    # For degree d, we need columns: x^d, x^(d-1), ..., x^1, x^0
    A = []
    for i in range(n):
        row = []
        for j in range(degree + 1):
            power = degree - j
            row.append(x_values[i] ** power)
        A.append(row)
    
    # Solve normal equation: (A^T A) coeffs = A^T y
    # First compute A^T A
    AtA = [[0.0] * (degree + 1) for _ in range(degree + 1)]
    for i in range(degree + 1):
        for j in range(degree + 1):
            for k in range(n):
                AtA[i][j] += A[k][i] * A[k][j]
    
    # Compute A^T y
    Aty = [0.0] * (degree + 1)
    for i in range(degree + 1):
        for k in range(n):
            Aty[i] += A[k][i] * y_values[k]
    
    # Solve using Gaussian elimination
    coeffs = gaussian_solve(AtA, Aty)
    
    # Calculate R-squared
    y_mean = sum(y_values) / n
    
    # Calculate predicted values
    y_pred = []
    for i in range(n):
        pred = 0.0
        for j in range(degree + 1):
            power = degree - j
            pred += coeffs[j] * (x_values[i] ** power)
        y_pred.append(pred)
    
    # Calculate R-squared
    ss_res = sum((y_values[i] - y_pred[i]) ** 2 for i in range(n))
    ss_tot = sum((y_values[i] - y_mean) ** 2 for i in range(n))
    
    if ss_tot == 0:
        r_squared = 1.0
    else:
        r_squared = 1.0 - ss_res / ss_tot
    
    # Format output
    result = {
        "coefficients": coeffs,
        "r_squared": r_squared
    }
    
    print(json.dumps(result, separators=(',', ':')))

def gaussian_solve(A, b):
    n = len(A)
    
    # Create augmented matrix
    aug = []
    for i in range(n):
        row = A[i][:] + [b[i]]
        aug.append(row)
    
    # Forward elimination
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(aug[k][i]) > abs(aug[max_row][i]):
                max_row = k
        
        # Swap rows
        aug[i], aug[max_row] = aug[max_row], aug[i]
        
        # Make diagonal 1
        pivot = aug[i][i]
        if abs(pivot) < 1e-10:
            continue
        
        for j in range(i, n + 1):
            aug[i][j] /= pivot
        
        # Eliminate column
        for k in range(n):
            if k != i:
                factor = aug[k][i]
                for j in range(i, n + 1):
                    aug[k][j] -= factor * aug[i][j]
    
    # Extract solution
    x = [aug[i][n] for i in range(n)]
    return x

solve_polynomial_regression()