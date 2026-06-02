import sys
import json
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def kmeans(points, k):
    # Initialize centroids - use first k points
    centroids = [points[i][:] for i in range(k)]
    
    for _ in range(100):  # max iterations
        # Assign points to clusters
        assignments = []
        for point in points:
            distances = [distance(point, centroid) for centroid in centroids]
            assignments.append(distances.index(min(distances)))
        
        # Update centroids
        new_centroids = []
        for i in range(k):
            cluster_points = [points[j] for j in range(len(points)) if assignments[j] == i]
            if cluster_points:
                new_centroid = [sum(p[0] for p in cluster_points) / len(cluster_points),
                               sum(p[1] for p in cluster_points) / len(cluster_points)]
                new_centroids.append(new_centroid)
            else:
                new_centroids.append(centroids[i][:])
        
        # Check convergence
        if all(distance(centroids[i], new_centroids[i]) < 1e-6 for i in range(k)):
            break
        
        centroids = new_centroids
    
    return centroids, assignments

# Read input
lines = sys.stdin.read().strip().split('\n')
k = int(lines[0])
points = []
for i in range(1, len(lines)):
    x, y = map(float, lines[i].split(','))
    points.append([x, y])

# Run k-means
centroids, assignments = kmeans(points, k)

# Output result
result = {
    "centroids": centroids,
    "assignments": assignments
}
print(json.dumps(result, separators=(',', ':')))