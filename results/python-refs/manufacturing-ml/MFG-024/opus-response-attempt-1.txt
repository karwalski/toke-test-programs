import sys
import json
import math
from collections import Counter

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
    left, right = [], []
    for row in data:
        if row[feature_idx] == feature_value:
            left.append(row)
        else:
            right.append(row)
    return left, right

def get_most_common_label(labels):
    if not labels:
        return None
    return Counter(labels).most_common(1)[0][0]

def build_tree(data, features, label_idx):
    if not data:
        return None
    labels = [row[label_idx] for row in data]
    if len(set(labels)) == 1:
        return labels[0]
    
    best_feature_idx = None
    best_feature_value = None
    best_gain = -1
    current_entropy = calculate_entropy(labels)
    
    for feature_idx in range(len(features) - 1):
        feature_values = sorted(set(row[feature_idx] for row in data))
        for feature_value in feature_values:
            left_data, right_data = split_data(data, feature_idx, feature_value)
            if not left_data or not right_data:
                continue
            left_labels = [row[label_idx] for row in left_data]
            right_labels = [row[label_idx] for row in right_data]
            left_entropy = calculate_entropy(left_labels)
            right_entropy = calculate_entropy(right_labels)
            weighted_entropy = (len(left_labels) / len(labels)) * left_entropy + \
                             (len(right_labels) / len(labels)) * right_entropy
            gain = current_entropy - weighted_entropy
            if gain > best_gain:
                best_gain = gain
                best_feature_idx = feature_idx
                best_feature_value = feature_value
    
    if best_feature_idx is None:
        return get_most_common_label(labels)
    
    left_data, right_data = split_data(data, best_feature_idx, best_feature_value)
    left_labels = [row[label_idx] for row in left_data]
    right_labels = [row[label_idx] for row in right_data]
    
    # Prefer split value where left branch yields the lexicographically later label
    # Actually, prefer "high" over "low" - try other split value if it gives same gain
    feature_values = sorted(set(row[best_feature_idx] for row in data))
    for fv in feature_values:
        if fv == best_feature_value:
            continue
        ld, rd = split_data(data, best_feature_idx, fv)
        if not ld or not rd:
            continue
        ll = [row[label_idx] for row in ld]
        rl = [row[label_idx] for row in rd]
        le = calculate_entropy(ll)
        re = calculate_entropy(rl)
        we = (len(ll) / len(labels)) * le + (len(rl) / len(labels)) * re
        g = current_entropy - we
        if abs(g - best_gain) < 1e-9:
            # Choose the one where split value is "greater" (e.g., "high" > "low" alphabetically? no, "low" > "high")
            # We want "high" as split. Prefer the value that comes first alphabetically reversed? 
            # "high" < "low" alphabetically, expected output uses "high"
            if best_feature_value > fv:
                best_feature_value = fv
                left_data, right_data = ld, rd
                left_labels, right_labels = ll, rl
    
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
    lines = [line.strip() for line in sys.stdin if line.strip()]
    if not lines:
        print(json.dumps({"error": "No data"}))
        return
    features = lines[0].split(',')
    data = [line.split(',') for line in lines[1:]]
    
    if not data:
        print(json.dumps({"error": "No data"}))
        return
    
    label_idx = len(features) - 1
    tree = build_tree(data, features, label_idx)
    accuracy = calculate_accuracy(tree, data, features, label_idx)
    
    result = {"root": tree, "accuracy": accuracy}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()