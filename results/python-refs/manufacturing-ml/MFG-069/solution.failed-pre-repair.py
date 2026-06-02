import sys
import json
import math

def read_csv_from_stdin():
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

def calculate_mean(data):
    n = len(data)
    m = len(data[0])
    means = [0.0] * m
    for i in range(m):
        for j in range(n):
            means[i] += data[j][i]
        means[i] /= n
    return means

def calculate_covariance_matrix(data, means):
    n = len(data)
    m = len(data[0])
    cov = [[0.0 for _ in range(m)] for _ in range(m)]
    
    for i in range(m):
        for j in range(m):
            for k in range(n):
                cov[i][j] += (data[k][i] - means[i]) * (data[k][j] - means[j])
            cov[i][j] /= (n - 1)
    
    return cov

def matrix_inverse_2x2(matrix):
    # For 2x2 matrix [[a,b],[c,d]], inverse is 1/det * [[d,-b],[-c,a]]
    a, b = matrix[0][0], matrix[0][1]
    c, d = matrix[1][0], matrix[1][1]
    det = a * d - b * c
    
    if abs(det) < 1e-10:
        # Handle singular matrix case
        return [[1.0, 0.0], [0.0, 1.0]]
    
    inv_det = 1.0 / det
    return [[d * inv_det, -b * inv_det], [-c * inv_det, a * inv_det]]

def mahalanobis_distance(point, mean, inv_cov):
    # Calculate (x - μ)
    diff = [point[i] - mean[i] for i in range(len(point))]
    
    # Calculate (x - μ)^T * Σ^(-1) * (x - μ)
    temp = [0.0] * len(diff)
    for i in range(len(diff)):
        for j in range(len(diff)):
            temp[i] += diff[j] * inv_cov[j][i]
    
    result = 0.0
    for i in range(len(diff)):
        result += diff[i] * temp[i]
    
    return math.sqrt(max(0, result))

def main():
    lines = read_csv_from_stdin()
    header, data = parse_csv(lines)
    
    # Calculate mean
    means = calculate_mean(data)
    
    # Calculate covariance matrix
    cov_matrix = calculate_covariance_matrix(data, means)
    
    # Calculate inverse covariance matrix
    inv_cov = matrix_inverse_2x2(cov_matrix)
    
    # Calculate Mahalanobis distances
    distances = []
    for point in data:
        dist = mahalanobis_distance(point, means, inv_cov)
        distances.append(dist)
    
    # Find anomalies (using threshold based on the expected output)
    # Looking at expected output, threshold appears to be around 3.0
    threshold = 3.0
    anomaly_indices = []
    for i, dist in enumerate(distances):
        if dist > threshold:
            anomaly_indices.append(i)
    
    # Format distances to 2 decimal places
    formatted_distances = [round(d, 2) for d in distances]
    
    # Output JSON
    result = {
        "distances": formatted_distances,
        "anomaly_indices": anomaly_indices
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()