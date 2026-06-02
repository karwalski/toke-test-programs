import sys
import csv
import json
from io import StringIO

def read_csv_data():
    """Read CSV data from stdin"""
    data = []
    reader = csv.DictReader(sys.stdin)
    for row in reader:
        data.append(row)
    return data

def prepare_design_matrix(data):
    """Prepare the design matrix X and response vector y for quadratic model"""
    n = len(data)
    # Get factor names (all columns except 'y')
    factor_names = [col for col in data[0].keys() if col != 'y']
    
    # Quadratic model: y = b0 + b1*x1 + b2*x2 + b11*x1^2 + b22*x2^2 + b12*x1*x2
    # Design matrix columns: [1, x1, x2, x1^2, x2^2, x1*x2]
    X = []
    y = []
    
    for row in data:
        x1 = float(row[factor_names[0]])
        x2 = float(row[factor_names[1]])
        response = float(row['y'])
        
        # Build row of design matrix
        x_row = [1, x1, x2, x1*x1, x2*x2, x1*x2]
        X.append(x_row)
        y.append(response)
    
    return X, y, factor_names

def matrix_multiply(A, B):
    """Multiply two matrices"""
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
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
    """Compute matrix inverse using Gaussian elimination"""
    n = len(matrix)
    # Create augmented matrix [A|I]
    augmented = []
    for i in range(n):
        row = matrix[i][:] + [0]*n
        row[n+i] = 1
        augmented.append(row)
    
    # Forward elimination
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(augmented[k][i]) > abs(augmented[max_row][i]):
                max_row = k
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        
        # Make diagonal 1
        pivot = augmented[i][i]
        for j in range(2*n):
            augmented[i][j] /= pivot
        
        # Eliminate column
        for k in range(n):
            if k != i:
                factor = augmented[k][i]
                for j in range(2*n):
                    augmented[k][j] -= factor * augmented[i][j]
    
    # Extract inverse matrix
    inverse = []
    for i in range(n):
        inverse.append(augmented[i][n:])
    
    return inverse

def fit_quadratic_model(X, y):
    """Fit quadratic response surface model using least squares"""
    # Convert to matrix form
    X_T = transpose(X)
    
    # Calculate (X'X)^-1 X' y
    XTX = matrix_multiply(X_T, X)
    XTX_inv = matrix_inverse(XTX)
    XTy = matrix_multiply(X_T, [[yi] for yi in y])
    coefficients = matrix_multiply(XTX_inv, XTy)
    
    # Flatten coefficients
    coefs = [row[0] for row in coefficients]
    return coefs

def find_optimum(coefficients):
    """Find optimum point by taking partial derivatives and setting to zero"""
    # Model: y = b0 + b1*x1 + b2*x2 + b11*x1^2 + b22*x2^2 + b12*x1*x2
    # Partial derivatives:
    # dy/dx1 = b1 + 2*b11*x1 + b12*x2 = 0
    # dy/dx2 = b2 + 2*b22*x2 + b12*x1 = 0
    
    b0, b1, b2, b11, b22, b12 = coefficients
    
    # Solve system of equations:
    # 2*b11*x1 + b12*x2 = -b1
    # b12*x1 + 2*b22*x2 = -b2
    
    # Matrix form: [2*b11  b12  ] [x1] = [-b1]
    #              [b12    2*b22] [x2]   [-b2]
    
    A = [[2*b11, b12], [b12, 2*b22]]
    b = [[-b1], [-b2]]
    
    A_inv = matrix_inverse(A)
    solution = matrix_multiply(A_inv, b)
    
    x1_opt = solution[0][0]
    x2_opt = solution[1][0]
    
    # Calculate predicted optimum value
    y_opt = b0 + b1*x1_opt + b2*x2_opt + b11*x1_opt*x1_opt + b22*x2_opt*x2_opt + b12*x1_opt*x2_opt
    
    return x1_opt, x2_opt, y_opt

def main():
    # Read data
    data = read_csv_data()
    
    # Prepare design matrix
    X, y, factor_names = prepare_design_matrix(data)
    
    # Fit quadratic model
    coefficients = fit_quadratic_model(X, y)
    
    # Find optimum
    x1_opt, x2_opt, y_opt = find_optimum(coefficients)
    
    # Prepare output
    result = {
        "optimum_point": {
            factor_names[0]: x1_opt,
            factor_names[1]: x2_opt
        },
        "predicted_optimum": y_opt
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()