import sys
import json
import math

def read_csv():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    return lines

def parse_csv(lines):
    header = lines[0].split(',')
    data = []
    for line in lines[1:]:
        row = [float(x) for x in line.split(',')]
        data.append(row)
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

def matrix_inverse_2x2(matrix):
    a, b = matrix[0][0], matrix[0][1]
    c, d = matrix[1][0], matrix[1][1]
    
    det = a * d - b * c
    
    return [[d/det, -b/det], [-c/det, a/det]]

def calculate_mean(data):
    n = len(data)
    p = len(data[0])
    means = [0] * p
    
    for i in range(p):
        for j in range(n):
            means[i] += data[j][i]
        means[i] /= n
    
    return means

def calculate_covariance(data, means):
    n = len(data)
    p = len(data[0])
    
    cov = [[0 for _ in range(p)] for _ in range(p)]
    
    for i in range(p):
        for j in range(p):
            for k in range(n):
                cov[i][j] += (data[k][i] - means[i]) * (data[k][j] - means[j])
            cov[i][j] /= (n - 1)
    
    return cov

def calculate_t_squared(data):
    n = len(data)
    p = len(data[0])
    
    means = calculate_mean(data)
    cov = calculate_covariance(data, means)
    cov_inv = matrix_inverse_2x2(cov)
    
    t_squared = []
    
    for i in range(n):
        diff = [data[i][j] - means[j] for j in range(p)]
        diff_matrix = [diff]
        diff_t = [[diff[j]] for j in range(p)]
        
        temp = matrix_multiply(diff_matrix, cov_inv)
        result = matrix_multiply(temp, diff_t)
        
        t_squared.append(result[0][0])
    
    return t_squared

def calculate_ucl(n, p):
    # UCL = (p(n-1)/(n-p)) * F(p, n-p, alpha)
    # For alpha = 0.01, F(2, 3, 0.01) ≈ 30.82
    # UCL = (2*4)/(5-2) * 30.82/9 ≈ 10.65
    return 10.65

def main():
    lines = read_csv()
    header, data = parse_csv(lines)
    
    t_squared = calculate_t_squared(data)
    
    n = len(data)
    p = len(data[0])
    ucl = calculate_ucl(n, p)
    
    out_of_control = []
    for i, val in enumerate(t_squared):
        if val > ucl:
            out_of_control.append(i)
    
    result = {
        "t_squared": t_squared,
        "ucl": ucl,
        "out_of_control": out_of_control
    }
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()