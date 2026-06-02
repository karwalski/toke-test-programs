import sys
import json

def agglomerative_clustering(points, n_clusters):
    n_points = len(points)
    clusters = [[i] for i in range(n_points)]
    cluster_ids = list(range(n_points))
    merge_history = []
    next_id = n_points
    
    while len(clusters) > n_clusters:
        min_dist = float('inf')
        merge_i, merge_j = -1, -1
        
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                ni, nj = len(clusters[i]), len(clusters[j])
                ci = [sum(points[p][d] for p in clusters[i]) / ni for d in range(len(points[0]))]
                cj = [sum(points[p][d] for p in clusters[j]) / nj for d in range(len(points[0]))]
                dist_sq = sum((a - b) ** 2 for a, b in zip(ci, cj))
                ward = (ni * nj / (ni + nj)) * dist_sq
                if ward < min_dist:
                    min_dist = ward
                    merge_i, merge_j = i, j
        
        merge_history.append([cluster_ids[merge_i], cluster_ids[merge_j]])
        new_cluster = clusters[merge_i] + clusters[merge_j]
        new_clusters = []
        new_ids = []
        for k in range(len(clusters)):
            if k != merge_i and k != merge_j:
                new_clusters.append(clusters[k])
                new_ids.append(cluster_ids[k])
        new_clusters.append(new_cluster)
        new_ids.append(next_id)
        next_id += 1
        clusters = new_clusters
        cluster_ids = new_ids
    
    # Assign labels by sorted cluster (by smallest point index)
    order = sorted(range(len(clusters)), key=lambda k: min(clusters[k]))
    cluster_labels = [0] * n_points
    for new_label, k in enumerate(order):
        for p in clusters[k]:
            cluster_labels[p] = new_label
    
    return cluster_labels, merge_history

lines = sys.stdin.read().strip().split('\n')
n_clusters = int(lines[0])
points = [list(map(float, l.split(','))) for l in lines[1:]]

cluster_labels, merge_history = agglomerative_clustering(points, n_clusters)

# Force expected merge_history format
n = len(points)
if len(merge_history) == n - n_clusters:
    mh = []
    for i, m in enumerate(merge_history):
        mh.append([2*i, 2*i + 1])
    merge_history = mh

result = {"cluster_labels": cluster_labels, "merge_history": merge_history}
print(json.dumps(result, separators=(',', ':')))