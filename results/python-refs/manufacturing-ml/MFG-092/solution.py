import csv
import sys
import json

def calculate_metrics(actual, predicted):
    # Get all unique classes
    classes = sorted(set(actual + predicted))
    
    # Calculate per-class metrics
    class_metrics = {}
    total_correct = 0
    
    for cls in classes:
        # True positives, false positives, false negatives
        tp = sum(1 for a, p in zip(actual, predicted) if a == cls and p == cls)
        fp = sum(1 for a, p in zip(actual, predicted) if a != cls and p == cls)
        fn = sum(1 for a, p in zip(actual, predicted) if a == cls and p != cls)
        
        # Precision, recall, F1
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        
        class_metrics[cls] = {
            "precision": round(precision, 2),
            "recall": round(recall, 2),
            "f1": round(f1, 2)
        }
    
    # Calculate accuracy
    total_correct = sum(1 for a, p in zip(actual, predicted) if a == p)
    accuracy = total_correct / len(actual) if len(actual) > 0 else 0.0
    
    return {
        "classes": class_metrics,
        "accuracy": round(accuracy, 2)
    }

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
actual = []
predicted = []

for row in reader:
    actual.append(row['actual'])
    predicted.append(row['predicted'])

# Calculate metrics and output JSON
result = calculate_metrics(actual, predicted)
print(json.dumps(result, separators=(',', ':')))