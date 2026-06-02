import sys
import json
import csv
from io import StringIO

def main():
    lines = sys.stdin.read().strip().split('\n')
    k = int(lines[0])
    
    # Parse CSV data
    csv_data = '\n'.join(lines[1:])
    csv_reader = csv.DictReader(StringIO(csv_data))
    
    data = list(csv_reader)
    n = len(data)
    
    # Extract features and targets
    X = []
    y = []
    for row in data:
        X.append(float(row['x']))
        y.append(float(row['y']))
    
    # Perform k-fold cross-validation
    fold_scores = []
    fold_size = n // k
    
    for i in range(k):
        # Define test indices for this fold
        start_idx = i * fold_size
        if i == k - 1:  # Last fold gets remaining data
            end_idx = n
        else:
            end_idx = (i + 1) * fold_size
        
        # Split data into train and test
        test_indices = set(range(start_idx, end_idx))
        
        X_train = []
        y_train = []
        X_test = []
        y_test = []
        
        for j in range(n):
            if j in test_indices:
                X_test.append(X[j])
                y_test.append(y[j])
            else:
                X_train.append(X[j])
                y_train.append(y[j])
        
        # Simple linear regression (least squares)
        # y = mx + b
        n_train = len(X_train)
        sum_x = sum(X_train)
        sum_y = sum(y_train)
        sum_xy = sum(x * y for x, y in zip(X_train, y_train))
        sum_xx = sum(x * x for x in X_train)
        
        # Calculate slope (m) and intercept (b)
        m = (n_train * sum_xy - sum_x * sum_y) / (n_train * sum_xx - sum_x * sum_x)
        b = (sum_y - m * sum_x) / n_train
        
        # Make predictions on test set
        y_pred = [m * x + b for x in X_test]
        
        # Calculate R² score
        y_test_mean = sum(y_test) / len(y_test)
        ss_tot = sum((y - y_test_mean) ** 2 for y in y_test)
        ss_res = sum((y_true - y_pred) ** 2 for y_true, y_pred in zip(y_test, y_pred))
        
        if ss_tot == 0:
            r2_score = 1.0
        else:
            r2_score = 1 - (ss_res / ss_tot)
        
        fold_scores.append(r2_score)
    
    # Calculate mean score
    mean_score = sum(fold_scores) / len(fold_scores)
    
    # Output result as JSON
    result = {
        "fold_scores": fold_scores,
        "mean_score": mean_score
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()