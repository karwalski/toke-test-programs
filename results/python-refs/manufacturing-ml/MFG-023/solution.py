import sys
import json
import math

def euclidean_distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def knn_classify(training_data, test_point, k=3):
    # Calculate distances from test point to all training points
    distances = []
    for features, label in training_data:
        dist = euclidean_distance(features, test_point)
        distances.append((dist, label))
    
    # Sort by distance and get k nearest neighbors
    distances.sort(key=lambda x: x[0])
    nearest_neighbors = [label for _, label in distances[:k]]
    
    # Predict class based on majority vote
    class_counts = {}
    for label in nearest_neighbors:
        class_counts[label] = class_counts.get(label, 0) + 1
    
    predicted_class = max(class_counts.keys(), key=lambda x: class_counts[x])
    
    return predicted_class, nearest_neighbors

# Read input from stdin
input_text = sys.stdin.read().strip()
lines = input_text.split('\n')

# Find separator
separator_index = lines.index('---')

# Parse training data
training_data = []
header = lines[0].split(',')
feature_count = len(header) - 1  # Exclude the class column

for i in range(1, separator_index):
    parts = lines[i].split(',')
    features = [float(x) for x in parts[:feature_count]]
    label = parts[-1]
    training_data.append((features, label))

# Parse test point
test_line = lines[separator_index + 1]
test_point = [float(x) for x in test_line.split(',')]

# Classify using KNN
predicted_class, nearest_neighbors = knn_classify(training_data, test_point)

# Output result as JSON
result = {
    "predicted_class": predicted_class,
    "nearest_neighbors": nearest_neighbors
}

print(json.dumps(result, separators=(',', ':')))