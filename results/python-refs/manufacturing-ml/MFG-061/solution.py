import csv
import sys
import json

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
data = list(reader)

# Initialize counters
tp = fp = tn = fn = 0

# Count true positives, false positives, true negatives, false negatives
for row in data:
    actual = row['actual']
    predicted = row['predicted']
    
    if actual == 'defect' and predicted == 'defect':
        tp += 1
    elif actual == 'ok' and predicted == 'defect':
        fp += 1
    elif actual == 'ok' and predicted == 'ok':
        tn += 1
    elif actual == 'defect' and predicted == 'ok':
        fn += 1

# Calculate metrics
total = tp + fp + tn + fn
accuracy = (tp + tn) / total if total > 0 else 0
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# Round to 2 decimal places
accuracy = round(accuracy, 2)
precision = round(precision, 2)
recall = round(recall, 2)
f1 = round(f1, 2)

# Create output dictionary
result = {
    "tp": tp,
    "fp": fp,
    "tn": tn,
    "fn": fn,
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1": f1
}

# Output JSON
print(json.dumps(result, separators=(',', ':')))