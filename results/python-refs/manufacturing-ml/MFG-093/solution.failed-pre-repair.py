import sys
import json
import math

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def kmeans(points, k, max_iterations=100):
    if k > len(points):
        k = len(points)
    
    # Initialize centroids by selecting first k points
    centroids = points[:k].copy()
    
    for _ in range(max_iterations):
        # Assign points to clusters
        clusters = [[] for _ in range(k)]
        for point in points:
            distances = [euclidean_distance(point, centroid) for centroid in centroids]
            closest_cluster = distances.index(min(distances))
            clusters[closest_cluster].append(point)
        
        # Update centroids
        new_centroids = []
        for i in range(k):
            if clusters[i]:
                x_avg = sum(p[0] for p in clusters[i]) / len(clusters[i])
                y_avg = sum(p[1] for p in clusters[i]) / len(clusters[i])
                new_centroids.append([x_avg, y_avg])
            else:
                new_centroids.append(centroids[i])
        
        # Check for convergence
        converged = True
        for i in range(k):
            if euclidean_distance(centroids[i], new_centroids[i]) > 1e-6:
                converged = False
                break
        
        centroids = new_centroids
        if converged:
            break
    
    return centroids, clusters

def calculate_wcss(clusters, centroids):
    wcss = 0
    for i, cluster in enumerate(clusters):
        for point in cluster:
            wcss += euclidean_distance(point, centroids[i])**2
    return wcss

def find_elbow(wcss_values):
    # Simple elbow detection: find point with maximum distance to line
    if len(wcss_values) < 3:
        return 1
    
    max_distance = -1
    elbow_k = 1
    
    for i in range(1, len(wcss_values) - 1):
        # Calculate distance from point to line connecting first and last points
        x1, y1 = 0, wcss_values[0]
        x2, y2 = len(wcss_values) - 1, wcss_values[-1]
        x0, y0 = i, wcss_values[i]
        
        # Distance from point to line formula
        if x2 - x1 == 0:
            distance = abs(x0 - x1)
        else:
            distance = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1) / math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        
        if distance > max_distance:
            max_distance = distance
            elbow_k = i + 1
    
    return elbow_k

# Read input
lines = sys.stdin.read().strip().split('\n')
max_k = int(lines[0])

# Parse data points
points = []
for line in lines[1:]:
    if line.strip():
        x, y = map(float, line.split(','))
        points.append([x, y])

# Calculate WCSS for each k
wcss_values = []
for k in range(1, max_k + 1):
    centroids, clusters = kmeans(points, k)
    wcss = calculate_wcss(clusters, centroids)
    wcss_values.append(round(wcss, 2))

# Find suggested k using elbow method
suggested_k = find_elbow(wcss_values)

# Output result
result = {
    "wcss": wcss_values,
    "suggested_k": suggested_k
}

print(json.dumps(result, separators=(',', ':')))