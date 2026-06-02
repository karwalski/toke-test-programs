import sys
import csv
import json
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def calculate_silhouette_scores(points, clusters):
    n = len(points)
    scores = []
    
    for i in range(n):
        current_cluster = clusters[i]
        current_point = points[i]
        
        # Calculate a(i) - mean distance to other points in same cluster
        same_cluster_distances = []
        for j in range(n):
            if i != j and clusters[j] == current_cluster:
                same_cluster_distances.append(distance(current_point, points[j]))
        
        if len(same_cluster_distances) == 0:
            a_i = 0
        else:
            a_i = sum(same_cluster_distances) / len(same_cluster_distances)
        
        # Calculate b(i) - mean distance to nearest other cluster
        other_clusters = set(clusters) - {current_cluster}
        min_avg_distance = float('inf')
        
        for other_cluster in other_clusters:
            other_cluster_distances = []
            for j in range(n):
                if clusters[j] == other_cluster:
                    other_cluster_distances.append(distance(current_point, points[j]))
            
            if other_cluster_distances:
                avg_distance = sum(other_cluster_distances) / len(other_cluster_distances)
                min_avg_distance = min(min_avg_distance, avg_distance)
        
        if min_avg_distance == float('inf'):
            b_i = 0
        else:
            b_i = min_avg_distance
        
        # Calculate silhouette score for this point
        if max(a_i, b_i) == 0:
            score = 0
        else:
            score = (b_i - a_i) / max(a_i, b_i)
        
        scores.append(score)
    
    return scores

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
points = []
clusters = []

for row in reader:
    x = float(row['x'])
    y = float(row['y'])
    cluster = int(row['cluster'])
    points.append((x, y))
    clusters.append(cluster)

# Calculate silhouette scores
per_point_scores = calculate_silhouette_scores(points, clusters)
overall_score = sum(per_point_scores) / len(per_point_scores) if per_point_scores else 0

# Round to 2 decimal places to match expected output
overall_score = round(overall_score, 2)
per_point_scores = [round(score, 2) for score in per_point_scores]

# Output JSON
result = {
    "silhouette_score": overall_score,
    "per_point_scores": per_point_scores
}

print(json.dumps(result, separators=(',', ':')))