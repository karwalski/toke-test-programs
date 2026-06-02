import sys
import csv
import json

def calculate_roc(actual, probabilities):
    P = sum(actual)
    N = len(actual) - P
    # group by unique threshold, sorted descending
    data = sorted(zip(probabilities, actual), key=lambda x: x[0], reverse=True)
    
    points = [{"fpr": 0.0, "tpr": 0.0}]
    tp = 0
    fp = 0
    i = 0
    n = len(data)
    while i < n:
        j = i
        while j < n and data[j][0] == data[i][0]:
            if data[j][1] == 1:
                tp += 1
            else:
                fp += 1
            j += 1
        fpr = fp / N if N > 0 else 0.0
        tpr = tp / P if P > 0 else 0.0
        points.append({"fpr": fpr, "tpr": tpr})
        i = j
    return points

def calc_auc(points):
    auc = 0.0
    for i in range(1, len(points)):
        x1, y1 = points[i-1]["fpr"], points[i-1]["tpr"]
        x2, y2 = points[i]["fpr"], points[i]["tpr"]
        auc += (x2 - x1) * (y1 + y2) / 2
    return auc

text = sys.stdin.read().strip()
lines = text.split('\n')
reader = csv.DictReader(lines)
actual = []
probs = []
for row in reader:
    actual.append(int(row['actual']))
    probs.append(float(row['probability']))

points = calculate_roc(actual, probs)
auc = calc_auc(points)

result = {"auc": auc, "roc_points": points}
print(json.dumps(result, separators=(',', ':')))