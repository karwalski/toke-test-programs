import sys
import json
import math

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse first line for n_components
    first_line = lines[0].split(',')
    n_components = int(first_line[1])
    
    # Parse header
    headers = lines[1].split(',')
    
    # Parse data
    data = []
    for i in range(2, len(lines)):
        row = [float(x) for x in lines[i].split(',')]
        data.append(row)
    
    return n_components, data

def mean_center_data(data):
    n_samples = len(data)
    n_features = len(data[0])
    
    # Calculate means
    means = [0.0] * n_features
    for row in data:
        for j in range(n_features):
            means[j] += row[j]
    
    for j in range(n_features):
        means[j] /= n_samples
    
    # Center the data
    centered_data = []
    for row in data:
        centered_row = []
        for j in range(n_features):
            centered_row.append(row[j] - means[j])
        centered_data.append(centered_row)
    
    return centered_data

def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    result = [[0.0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

def transpose(matrix):
    rows, cols = len(matrix), len(matrix[0])
    return [[matrix[i][j] for i in range(rows)] for j in range(cols)]

def covariance_matrix(data):
    n_samples = len(data)
    data_T = transpose(data)
    
    # Compute data_T @ data / (n_samples - 1)
    cov = matrix_multiply(data_T, data)
    
    # Divide by (n_samples - 1)
    for i in range(len(cov)):
        for j in range(len(cov[0])):
            cov[i][j] /= (n_samples - 1)
    
    return cov

def power_iteration(matrix, num_iterations=1000):
    n = len(matrix)
    # Start with random vector
    v = [1.0] * n
    
    for _ in range(num_iterations):
        # Matrix-vector multiplication
        Av = [0.0] * n
        for i in range(n):
            for j in range(n):
                Av[i] += matrix[i][j] * v[j]
        
        # Calculate norm
        norm = math.sqrt(sum(x * x for x in Av))
        
        # Normalize
        if norm > 0:
            v = [x / norm for x in Av]
        
        # Check convergence (simplified)
        if _ > 10:  # Simple convergence check
            break
    
    # Calculate eigenvalue
    Av = [0.0] * n
    for i in range(n):
        for j in range(n):
            Av[i] += matrix[i][j] * v[j]
    
    eigenvalue = sum(v[i] * Av[i] for i in range(n))
    
    return eigenvalue, v

def deflate_matrix(matrix, eigenvalue, eigenvector):
    n = len(matrix)
    # Create outer product of eigenvector
    outer = [[eigenvector[i] * eigenvector[j] for j in range(n)] for i in range(n)]
    
    # Subtract eigenvalue * outer product from matrix
    deflated = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            deflated[i][j] = matrix[i][j] - eigenvalue * outer[i][j]
    
    return deflated

def pca(data, n_components):
    # Mean center the data
    centered_data = mean_center_data(data)
    
    # Compute covariance matrix
    cov_matrix = covariance_matrix(centered_data)
    
    eigenvalues = []
    eigenvectors = []
    
    # Find first n_components eigenvalues and eigenvectors
    current_matrix = [row[:] for row in cov_matrix]  # Deep copy
    
    for _ in range(n_components):
        eigenvalue, eigenvector = power_iteration(current_matrix)
        eigenvalues.append(eigenvalue)
        eigenvectors.append(eigenvector)
        
        # Deflate matrix for next iteration
        current_matrix = deflate_matrix(current_matrix, eigenvalue, eigenvector)
    
    # Transform data
    eigenvector_matrix = transpose(eigenvectors)
    transformed_data = matrix_multiply(centered_data, eigenvector_matrix)
    
    # Calculate explained variance ratio
    total_variance = sum(eigenvalues)
    explained_variance_ratio = [ev / total_variance for ev in eigenvalues]
    
    return transformed_data, explained_variance_ratio

def main():
    n_components, data = read_input()
    transformed_data, explained_variance_ratio = pca(data, n_components)
    
    # Round to 2 decimal places and format
    transformed_rounded = [[round(x, 2) for x in row] for row in transformed_data]
    explained_variance_rounded = [round(x, 1) for x in explained_variance_ratio]
    
    result = {
        "transformed": transformed_rounded,
        "explained_variance_ratio": explained_variance_rounded
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()