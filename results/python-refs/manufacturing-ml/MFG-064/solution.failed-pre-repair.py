import sys
import json
import math

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Find the separator
    try:
        separator_idx = lines.index('---')
    except ValueError:
        raise ValueError("Separator '---' not found in input")
    
    # Parse training data
    training_lines = lines[:separator_idx]
    if len(training_lines) < 2:
        raise ValueError("Insufficient training data")
        
    header = training_lines[0].split(',')
    data_lines = training_lines[1:]
    
    training_data = []
    for line in data_lines:
        if not line.strip():
            continue
        values = line.split(',')
        if len(values) != len(header):
            continue
        row = {}
        try:
            for i, col in enumerate(header):
                if col == 'class':
                    row[col] = values[i].strip()
                else:
                    row[col] = float(values[i].strip())
            training_data.append(row)
        except (ValueError, IndexError):
            continue
    
    # Parse test point
    if separator_idx + 1 >= len(lines):
        raise ValueError("No test point provided")
        
    test_line = lines[separator_idx + 1]
    try:
        test_values = [float(x.strip()) for x in test_line.split(',')]
    except ValueError:
        raise ValueError("Invalid test point format")
    
    feature_names = [col for col in header if col != 'class']
    
    if len(test_values) != len(feature_names):
        raise ValueError("Test point dimension mismatch")
    
    return training_data, test_values, feature_names

def gaussian_naive_bayes(training_data, test_point, feature_names):
    if not training_data:
        raise ValueError("No training data available")
    
    # Get unique classes
    classes = list(set(row['class'] for row in training_data))
    if not classes:
        raise ValueError("No classes found")
    
    # Calculate class probabilities and feature statistics
    class_stats = {}
    total_samples = len(training_data)
    
    for cls in classes:
        class_data = [row for row in training_data if row['class'] == cls]
        class_count = len(class_data)
        
        if class_count == 0:
            continue
            
        class_stats[cls] = {
            'prior': class_count / total_samples,
            'features': {}
        }
        
        # Calculate mean and std for each feature
        for feature in feature_names:
            values = [row[feature] for row in class_data]
            if not values:
                continue
                
            mean = sum(values) / len(values)
            
            # Calculate standard deviation
            if len(values) == 1:
                std = 1e-6  # Single sample, use small std
            else:
                variance = sum((x - mean) ** 2 for x in values) / len(values)
                std = math.sqrt(variance) if variance > 0 else 1e-6
            
            class_stats[cls]['features'][feature] = {
                'mean': mean,
                'std': std
            }
    
    # Calculate probabilities for test point
    class_probabilities = {}
    
    for cls in classes:
        if cls not in class_stats:
            continue
            
        # Start with log prior
        log_prob = math.log(class_stats[cls]['prior'])
        
        # Add log likelihood for each feature
        for i, feature in enumerate(feature_names):
            if feature not in class_stats[cls]['features']:
                continue
                
            mean = class_stats[cls]['features'][feature]['mean']
            std = class_stats[cls]['features'][feature]['std']
            
            # Gaussian probability density function
            exponent = -0.5 * ((test_point[i] - mean) / std) ** 2
            coefficient = 1 / (std * math.sqrt(2 * math.pi))
            
            likelihood = coefficient * math.exp(exponent)
            
            # Ensure likelihood is positive and not too small
            likelihood = max(likelihood, 1e-10)
            
            log_prob += math.log(likelihood)
        
        class_probabilities[cls] = log_prob
    
    # Convert log probabilities to actual probabilities
    # Subtract max for numerical stability
    max_log_prob = max(class_probabilities.values())
    exp_probs = {}
    
    for cls, log_prob in class_probabilities.items():
        exp_probs[cls] = math.exp(log_prob - max_log_prob)
    
    # Normalize
    total_prob = sum(exp_probs.values())
    if total_prob == 0:
        # Equal probabilities if all are zero
        normalized_probs = {cls: 1.0 / len(exp_probs) for cls in exp_probs}
    else:
        normalized_probs = {cls: prob / total_prob for cls, prob in exp_probs.items()}
    
    # Find predicted class
    predicted_class = max(normalized_probs, key=normalized_probs.get)
    
    # Round probabilities to 2 decimal places
    rounded_probs = {cls: round(prob, 2) for cls, prob in normalized_probs.items()}
    
    return predicted_class, rounded_probs

def main():
    try:
        training_data, test_point, feature_names = read_input()
        predicted_class, probabilities = gaussian_naive_bayes(training_data, test_point, feature_names)
        
        result = {
            "predicted_class": predicted_class,
            "probabilities": probabilities
        }
        
        print(json.dumps(result))
        
    except Exception as e:
        # Return error in expected format
        result = {
            "predicted_class": "ERROR",
            "probabilities": {}
        }
        print(json.dumps(result))

if __name__ == "__main__":
    main()