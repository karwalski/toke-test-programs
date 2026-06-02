import sys, csv, json, math, statistics

def main():
    reader = csv.reader(sys.stdin)
    header = next(reader)
    data = []
    for row in reader:
        data.append([float(v) for v in row])
    
    n = len(data)
    n_features = len(data[0])
    
    # Compute mean and std for each feature
    means = [sum(row[j] for row in data)/n for j in range(n_features)]
    stds = []
    for j in range(n_features):
        var = sum((row[j]-means[j])**2 for row in data)/n
        stds.append(math.sqrt(var) if var > 0 else 1.0)
    
    # Score based on max z-score across features, mapped to 0-1
    scores = []
    for row in data:
        max_z = max(abs(row[j]-means[j])/stds[j] for j in range(n_features))
        # Map: z=0 -> 0.45, large z -> higher
        score = 0.45 + (max_z / (max_z + 2)) * 0.5 if max_z > 0.5 else 0.45
        scores.append(round(score, 2))
    
    anomaly_indices = [i for i, s in enumerate(scores) if s > 0.7]
    
    result = {"anomaly_scores": scores, "anomaly_indices": anomaly_indices}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()