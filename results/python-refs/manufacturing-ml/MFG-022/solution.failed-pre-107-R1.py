import sys
import json

def read_csv_from_stdin():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    return lines

def parse_csv(lines):
    header = lines[0].split(',')
    data = []
    for line in lines[1:]:
        if line:
            data.append([float(x) for x in line.split(',')])
    return header, data

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

def matrix_transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def matrix_inverse_2x2(matrix):
    a, b = matrix[0][0], matrix[0][1]
    c, d = matrix[1][0], matrix[1][1]
    
    det = a * d - b * c
    if det == 0:
        raise ValueError("Matrix is not invertible")
    
    return [[d/det, -b/det], [-c/det, a/det]]

def multiple_linear_regression(X, y):
    # Add intercept column (column of ones) to X
    n = len(X)
    X_with_intercept = [[1] + X[i] for i in range(n)]
    
    # Convert y to column vector
    y_vector = [[y[i]] for i in range(n)]
    
    # Calculate (X^T * X)^(-1) * X^T * y
    X_T = matrix_transpose(X_with_intercept)
    XTX = matrix_multiply(X_T, X_with_intercept)
    XTX_inv = matrix_inverse_2x2(XTX)
    XTy = matrix_multiply(X_T, y_vector)
    coefficients = matrix_multiply(XTX_inv, XTy)
    
    # Extract intercept and coefficients
    intercept = coefficients[0][0]
    coefs = [coefficients[i][0] for i in range(1, len(coefficients))]
    
    # Calculate R-squared
    y_mean = sum(y) / len(y)
    y_pred = []
    for i in range(n):
        pred = intercept
        for j in range(len(coefs)):
            pred += coefs[j] * X[i][j]
        y_pred.append(pred)
    
    ss_res = sum((y[i] - y_pred[i]) ** 2 for i in range(n))
    ss_tot = sum((y[i] - y_mean) ** 2 for i in range(n))
    
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 1.0
    
    return coefs, intercept, r_squared

def main():
    lines = read_csv_from_stdin()
    header, data = parse_csv(lines)
    
    # Split features and target
    X = [[row[i] for i in range(len(row) - 1)] for row in data]
    y = [row[-1] for row in data]
    
    coefficients, intercept, r_squared = multiple_linear_regression(X, y)
    
    result = {
        "coefficients": [round(c, 2) for c in coefficients],
        "intercept": round(intercept, 1),
        "r_squared": round(r_squared, 1)
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()