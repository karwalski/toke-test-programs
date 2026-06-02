import csv
import sys
import json
import math

def main():
    reader = csv.reader(sys.stdin)
    rows = list(reader)
    headers = rows[0]
    data_rows = rows[1:]
    feature_names = headers[:-1]
    
    features = {name: [] for name in feature_names}
    target = []
    
    for row in data_rows:
        for i, name in enumerate(feature_names):
            features[name].append(float(row[i]))
        target.append(float(row[-1]))
    
    n = len(target)
    mean_y = sum(target) / n
    sum_sq_y = sum((y - mean_y) ** 2 for y in target)
    
    importances = {}
    for feature_name, feature_values in features.items():
        mean_x = sum(feature_values) / n
        sum_sq_x = sum((x - mean_x) ** 2 for x in feature_values)
        numerator = sum((feature_values[i] - mean_x) * (target[i] - mean_y) for i in range(n))
        denom = math.sqrt(sum_sq_x * sum_sq_y)
        if denom == 0:
            corr = 0
        else:
            corr = numerator / denom
        # Use r^2 as importance
        importances[feature_name] = corr * corr
    
    total = sum(importances.values())
    if total > 0:
        for k in importances:
            importances[k] /= total
    
    feature_importances = [{"feature": f, "importance": round(v, 1)} for f, v in importances.items()]
    feature_importances.sort(key=lambda x: x["importance"], reverse=True)
    
    print(json.dumps({"feature_importances": feature_importances}, separators=(',', ':')))

if __name__ == "__main__":
    main()