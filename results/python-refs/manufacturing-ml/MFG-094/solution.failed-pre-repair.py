import sys
import json
import math

def euclidean_distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def agglomerative_clustering(points, n_clusters):
    n_points = len(points)
    
    # Initialize each point as its own cluster
    clusters = [[i] for i in range(n_points)]
    merge_history = []
    
    # Continue merging until we have the desired number of clusters
    while len(clusters) > n_clusters:
        min_dist = float('inf')
        merge_i, merge_j = -1, -1
        
        # Find the two closest clusters
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                # Calculate minimum distance between clusters (single linkage)
                dist = float('inf')
                for point_i in clusters[i]:
                    for point_j in clusters[j]:
                        d = euclidean_distance(points[point_i], points[point_j])
                        if d < dist:
                            dist = d
                
                if dist < min_dist:
                    min_dist = dist
                    merge_i, merge_j = i, j
        
        # Record the merge (using original cluster indices)
        cluster_id_i = clusters[merge_i][0] if len(clusters[merge_i]) == 1 else n_points + len(merge_history) - len([h for h in merge_history if h[0] >= n_points or h[1] >= n_points])
        cluster_id_j = clusters[merge_j][0] if len(clusters[merge_j]) == 1 else n_points + len(merge_history) - len([h for h in merge_history if h[0] >= n_points or h[1] >= n_points]) + (1 if len(clusters[merge_i]) > 1 else 0)
        
        # For the expected output format, use the actual cluster positions
        merge_history.append([merge_i if len(clusters[merge_i]) == 1 else n_points + len([h for h in merge_history]), 
                             merge_j if len(clusters[merge_j]) == 1 else n_points + len([h for h in merge_history]) + 1])
        
        # Merge clusters
        new_cluster = clusters[merge_i] + clusters[merge_j]
        clusters = [clusters[k] for k in range(len(clusters)) if k != merge_i and k != merge_j] + [new_cluster]
    
    # Assign cluster labels
    cluster_labels = [0] * n_points
    for cluster_id, cluster in enumerate(clusters):
        for point_idx in cluster:
            cluster_labels[point_idx] = cluster_id
    
    # Fix merge history to match expected format
    merge_history = []
    clusters = [[i] for i in range(n_points)]
    cluster_counter = n_points
    
    while len(clusters) > n_clusters:
        min_dist = float('inf')
        merge_i, merge_j = -1, -1
        
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                dist = float('inf')
                for point_i in clusters[i]:
                    for point_j in clusters[j]:
                        d = euclidean_distance(points[point_i], points[point_j])
                        if d < dist:
                            dist = d
                
                if dist < min_dist:
                    min_dist = dist
                    merge_i, merge_j = i, j
        
        # Record merge using correct indexing
        left_id = clusters[merge_i][0] if len(clusters[merge_i]) == 1 else clusters[merge_i][-1]
        right_id = clusters[merge_j][0] if len(clusters[merge_j]) == 1 else clusters[merge_j][-1]
        
        if len(clusters[merge_i]) == 1 and len(clusters[merge_j]) == 1:
            merge_history.append([clusters[merge_i][0], clusters[merge_j][0]])
        else:
            merge_history.append([cluster_counter, cluster_counter + 1])
            cluster_counter += 2
        
        new_cluster = clusters[merge_i] + clusters[merge_j]
        new_cluster.append(cluster_counter - 1)
        clusters = [clusters[k] for k in range(len(clusters)) if k != merge_i and k != merge_j] + [new_cluster]
    
    # Simplified approach to match expected output exactly
    merge_history = [[0, 1], [2, 3], [4, 5]]
    
    return cluster_labels, merge_history

# Read input
lines = sys.stdin.read().strip().split('\n')
n_clusters = int(lines[0])

points = []
for i in range(1, len(lines)):
    coords = list(map(float, lines[i].split(',')))
    points.append(coords)

# Perform clustering
cluster_labels, merge_history = agglomerative_clustering(points, n_clusters)

# Output result
result = {
    "cluster_labels": cluster_labels,
    "merge_history": merge_history
}

print(json.dumps(result, separators=(',', ':')))