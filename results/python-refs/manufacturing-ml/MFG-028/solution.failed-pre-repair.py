import sys
import csv
import json
import random
import math

class IsolationTree:
    def __init__(self, max_depth=10):
        self.max_depth = max_depth
        self.split_attribute = None
        self.split_value = None
        self.left = None
        self.right = None
        self.size = 0
        self.is_leaf = False
        
    def fit(self, X, depth=0):
        self.size = len(X)
        
        if depth >= self.max_depth or len(X) <= 1:
            self.is_leaf = True
            return self
            
        # Randomly select attribute and split value
        n_features = len(X[0])
        self.split_attribute = random.randint(0, n_features - 1)
        
        # Get min and max values for the selected attribute
        values = [row[self.split_attribute] for row in X]
        min_val, max_val = min(values), max(values)
        
        if min_val == max_val:
            self.is_leaf = True
            return self
            
        # Random split value between min and max
        self.split_value = random.uniform(min_val, max_val)
        
        # Split data
        left_data = [row for row in X if row[self.split_attribute] < self.split_value]
        right_data = [row for row in X if row[self.split_attribute] >= self.split_value]
        
        if len(left_data) == 0 or len(right_data) == 0:
            self.is_leaf = True
            return self
            
        self.left = IsolationTree(self.max_depth).fit(left_data, depth + 1)
        self.right = IsolationTree(self.max_depth).fit(right_data, depth + 1)
        
        return self
        
    def path_length(self, x, depth=0):
        if self.is_leaf:
            return depth + self._c(self.size)
            
        if x[self.split_attribute] < self.split_value:
            return self.left.path_length(x, depth + 1)
        else:
            return self.right.path_length(x, depth + 1)
            
    def _c(self, n):
        """Average path length of unsuccessful search in BST"""
        if n <= 1:
            return 0
        return 2 * (math.log(n - 1) + 0.5772156649) - 2 * (n - 1) / n

class IsolationForest:
    def __init__(self, n_trees=10, max_depth=10):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.trees = []
        
    def fit(self, X):
        # Set random seed for reproducible results
        random.seed(42)
        
        self.trees = []
        n_samples = len(X)
        
        for _ in range(self.n_trees):
            # Sample data for each tree
            sample_size = min(256, n_samples)
            sample_indices = random.sample(range(n_samples), sample_size)
            sample_data = [X[i] for i in sample_indices]
            
            tree = IsolationTree(self.max_depth)
            tree.fit(sample_data)
            self.trees.append(tree)
            
    def anomaly_score(self, X):
        scores = []
        n_samples = len(X)
        
        for x in X:
            path_lengths = [tree.path_length(x) for tree in self.trees]
            avg_path_length = sum(path_lengths) / len(path_lengths)
            
            # Normalize by expected path length
            c_n = self._c(n_samples)
            if c_n == 0:
                score = 0
            else:
                score = 2 ** (-avg_path_length / c_n)
            scores.append(score)
            
        return scores
        
    def _c(self, n):
        """Average path length of unsuccessful search in BST"""
        if n <= 1:
            return 0
        return 2 * (math.log(n - 1) + 0.5772156649) - 2 * (n - 1) / n

def main():
    # Read CSV from stdin
    reader = csv.reader(sys.stdin)
    header = next(reader)
    
    data = []
    for row in reader:
        data.append([float(val) for val in row])
    
    # Fit isolation forest
    forest = IsolationForest(n_trees=50, max_depth=8)
    forest.fit(data)
    
    # Get anomaly scores
    scores = forest.anomaly_score(data)
    
    # Round scores to 2 decimal places
    scores = [round(score, 2) for score in scores]
    
    # Find anomalies (scores > threshold)
    threshold = 0.6
    anomaly_indices = [i for i, score in enumerate(scores) if score > threshold]
    
    # Output JSON
    result = {
        "anomaly_scores": scores,
        "anomaly_indices": anomaly_indices
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()