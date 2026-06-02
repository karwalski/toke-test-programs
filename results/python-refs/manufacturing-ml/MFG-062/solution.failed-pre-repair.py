import sys
import csv
import json

def calculate_roc_curve(actual, probabilities):
    # Combine actual and probabilities, sort by probability descending
    data = list(zip(actual, probabilities))
    data.sort(key=lambda x: x[1], reverse=True)
    
    # Calculate total positives and negatives
    total_positives = sum(actual)
    total_negatives = len(actual) - total_positives
    
    # Initialize counters
    tp = 0  # true positives
    fp = 0  # false positives
    
    roc_points = []
    prev_threshold = float('inf')
    
    # Add starting point (0, 0)
    roc_points.append({"fpr": 0.0, "tpr": 0.0})
    
    for i, (label, prob) in enumerate(data):
        # If probability changed, add current point
        if prob != prev_threshold and i > 0:
            fpr = fp / total_negatives if total_negatives > 0 else 0.0
            tpr = tp / total_positives if total_positives > 0 else 0.0
            roc_points.append({"fpr": fpr, "tpr": tpr})
        
        # Update counters
        if label == 1:
            tp += 1
        else:
            fp += 1
        
        prev_threshold = prob
    
    # Add final point
    fpr = fp / total_negatives if total_negatives > 0 else 0.0
    tpr = tp / total_positives if total_positives > 0 else 0.0
    roc_points.append({"fpr": fpr, "tpr": tpr})
    
    return roc_points

def calculate_auc(roc_points):
    auc = 0.0
    for i in range(1, len(roc_points)):
        x1, y1 = roc_points[i-1]["fpr"], roc_points[i-1]["tpr"]
        x2, y2 = roc_points[i]["fpr"], roc_points[i]["tpr"]
        auc += (x2 - x1) * (y1 + y2) / 2
    return auc

# Read input
input_text = sys.stdin.read().strip()
lines = input_text.split('\n')
reader = csv.DictReader(lines)

actual = []
probabilities = []

for row in reader:
    actual.append(int(row['actual']))
    probabilities.append(float(row['probability']))

# Calculate ROC curve points
roc_points = calculate_roc_curve(actual, probabilities)

# Calculate AUC
auc = calculate_auc(roc_points)

# Output result
result = {
    "auc": auc,
    "roc_points": roc_points
}

print(json.dumps(result, separators=(',', ':')))