import sys
import json
import math
from collections import Counter

def read_csv_from_stdin():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    return lines

def parse_csv(lines):
    if not lines:
        return [], []
    
    header = lines[0].split(',')
    data = []
    for line in lines[1:]:
        data.append(line.split(','))
    
    return header, data

def calculate_entropy(labels):
    if not labels:
        return 0
    
    counts = Counter(labels)
    total = len(labels)
    entropy = 0
    
    for count in counts.values():
        prob = count / total
        if prob > 0:
            entropy -= prob * math.log2(prob)
    
    return entropy

def split_data(data, feature_idx, feature_value):
    left = []
    right = []
    
    for row in data:
        if row[feature_idx] == feature_value:
            left.append(row)
        else:
            right.append(row)
    
    return left, right

def get_most_common_label(labels):
    if not labels:
        return None
    counter = Counter(labels)
    return counter.most_common(1)[0][0]

def build_tree(data, features, label_idx):
    if not data:
        return None
    
    # Get all labels
    labels = [row[label_idx] for row in data]
    
    # If all labels are the same, return leaf
    unique_labels = set(labels)
    if len(unique_labels) == 1:
        return labels[0]
    
    # Find best split
    best_feature_idx = None
    best_feature_value = None
    best_gain = -1
    
    current_entropy = calculate_entropy(labels)
    
    for feature_idx in range(len(features) - 1):  # Exclude label column
        # Get unique values for this feature
        feature_values = set(row[feature_idx] for row in data)
        
        for feature_value in feature_values:
            left_data, right_data = split_data(data, feature_idx, feature_value)
            
            if not left_data or not right_data:
                continue
            
            left_labels = [row[label_idx] for row in left_data]
            right_labels = [row[label_idx] for row in right_data]
            
            # Calculate information gain
            left_entropy = calculate_entropy(left_labels)
            right_entropy = calculate_entropy(right_labels)
            
            weighted_entropy = (len(left_labels) / len(labels)) * left_entropy + \
                             (len(right_labels) / len(labels)) * right_entropy
            
            gain = current_entropy - weighted_entropy
            
            if gain > best_gain:
                best_gain = gain
                best_feature_idx = feature_idx
                best_feature_value = feature_value
    
    # If no good split found, return most common label
    if best_feature_idx is None:
        return get_most_common_label(labels)
    
    # Create split
    left_data, right_data = split_data(data, best_feature_idx, best_feature_value)
    
    left_labels = [row[label_idx] for row in left_data]
    right_labels = [row[label_idx] for row in right_data]
    
    # For simple binary classification, return the prediction directly
    left_prediction = get_most_common_label(left_labels)
    right_prediction = get_most_common_label(right_labels)
    
    return {
        "feature": features[best_feature_idx],
        "split": best_feature_value,
        "left": left_prediction,
        "right": right_prediction
    }

def predict(tree, row, features):
    if isinstance(tree, str):
        return tree
    
    feature_idx = features.index(tree["feature"])
    if row[feature_idx] == tree["split"]:
        return tree["left"]
    else:
        return tree["right"]

def calculate_accuracy(tree, data, features, label_idx):
    if not data:
        return 0.0
    
    correct = 0
    for row in data:
        predicted = predict(tree, row, features)
        actual = row[label_idx]
        if predicted == actual:
            correct += 1
    
    return correct / len(data)

def main():
    lines = read_csv_from_stdin()
    features, data = parse_csv(lines)
    
    if not data:
        print(json.dumps({"error": "No data"}))
        return
    
    label_idx = len(features) - 1  # Last column is label
    
    tree = build_tree(data, features, label_idx)
    accuracy = calculate_accuracy(tree, data, features, label_idx)
    
    result = {
        "root": tree,
        "accuracy": accuracy
    }
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()