import csv
import sys
import json
import math

def calculate_variance(values):
    if len(values) <= 1:
        return 0
    mean = sum(values) / len(values)
    return sum((x - mean) ** 2 for x in values) / len(values)

def calculate_feature_importance(features, target):
    # Calculate correlation-based importance
    importances = {}
    
    for feature_name, feature_values in features.items():
        # Calculate correlation coefficient
        n = len(feature_values)
        if n <= 1:
            importances[feature_name] = 0.0
            continue
            
        # Calculate means
        mean_x = sum(feature_values) / n
        mean_y = sum(target) / n
        
        # Calculate correlation coefficient
        numerator = sum((feature_values[i] - mean_x) * (target[i] - mean_y) for i in range(n))
        
        sum_sq_x = sum((x - mean_x) ** 2 for x in feature_values)
        sum_sq_y = sum((y - mean_y) ** 2 for y in target)
        
        denominator = math.sqrt(sum_sq_x * sum_sq_y)
        
        if denominator == 0:
            correlation = 0
        else:
            correlation = numerator / denominator
        
        # Use absolute correlation as importance
        importances[feature_name] = abs(correlation)
    
    # Normalize importances so they sum to 1 (if any are non-zero)
    total_importance = sum(importances.values())
    if total_importance > 0:
        for feature in importances:
            importances[feature] = importances[feature] / total_importance
    
    return importances

def main():
    # Read CSV from stdin
    reader = csv.reader(sys.stdin)
    rows = list(reader)
    
    if len(rows) < 2:
        print('{"feature_importances":[]}')
        return
    
    headers = rows[0]
    data_rows = rows[1:]
    
    # Assume last column is target
    feature_names = headers[:-1]
    target_name = headers[-1]
    
    # Parse data
    features = {name: [] for name in feature_names}
    target = []
    
    for row in data_rows:
        for i, name in enumerate(feature_names):
            features[name].append(float(row[i]))
        target.append(float(row[-1]))
    
    # Calculate feature importances
    importances = calculate_feature_importance(features, target)
    
    # Create output format
    feature_importances = []
    for feature, importance in importances.items():
        feature_importances.append({
            "feature": feature,
            "importance": round(importance, 1)
        })
    
    # Sort by importance descending
    feature_importances.sort(key=lambda x: x["importance"], reverse=True)
    
    result = {"feature_importances": feature_importances}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()