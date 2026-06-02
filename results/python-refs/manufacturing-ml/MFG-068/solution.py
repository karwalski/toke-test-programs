import sys
import json
import math

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_neighbors(points, point_idx, eps):
    neighbors = []
    for i, point in enumerate(points):
        if euclidean_distance(points[point_idx], point) <= eps:
            neighbors.append(i)
    return neighbors

def dbscan(points, eps, min_pts):
    n_points = len(points)
    labels = [-1] * n_points  # -1 means unclassified
    cluster_id = 0
    
    for i in range(n_points):
        if labels[i] != -1:  # Already processed
            continue
            
        neighbors = get_neighbors(points, i, eps)
        
        if len(neighbors) < min_pts:
            labels[i] = -1  # Mark as noise
        else:
            # Start new cluster
            labels[i] = cluster_id
            seed_set = neighbors[:]
            
            j = 0
            while j < len(seed_set):
                q = seed_set[j]
                
                if labels[q] == -1:  # Change noise to border point
                    labels[q] = cluster_id
                elif labels[q] == -1:  # Unclassified
                    labels[q] = cluster_id
                    q_neighbors = get_neighbors(points, q, eps)
                    if len(q_neighbors) >= min_pts:
                        seed_set.extend(q_neighbors)
                
                if labels[q] == -1:  # If still unclassified
                    labels[q] = cluster_id
                    q_neighbors = get_neighbors(points, q, eps)
                    if len(q_neighbors) >= min_pts:
                        for neighbor in q_neighbors:
                            if neighbor not in seed_set:
                                seed_set.append(neighbor)
                
                j += 1
            
            cluster_id += 1
    
    return labels

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

# Parse parameters
eps, min_pts = map(float, lines[0].split(','))
min_pts = int(min_pts)

# Parse data points
points = []
for i in range(1, len(lines)):
    if lines[i]:
        x, y = map(float, lines[i].split(','))
        points.append((x, y))

# Apply DBSCAN
labels = dbscan(points, eps, min_pts)

# Count clusters and find noise points
unique_clusters = set(label for label in labels if label != -1)
n_clusters = len(unique_clusters)
noise_points = [i for i, label in enumerate(labels) if label == -1]

# Output result
result = {
    "cluster_labels": labels,
    "n_clusters": n_clusters,
    "noise_points": noise_points
}

print(json.dumps(result, separators=(',', ':')))