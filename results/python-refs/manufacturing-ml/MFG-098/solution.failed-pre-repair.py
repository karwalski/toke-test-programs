import sys
import json
from itertools import product

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Find where response data starts
    response_idx = None
    for i, line in enumerate(lines):
        if line == 'response':
            response_idx = i
            break
    
    # Parse factors
    factors = {}
    factor_names = []
    for i in range(1, response_idx):
        parts = lines[i].split(',')
        factor_name = parts[0]
        low = float(parts[1])
        high = float(parts[2])
        factors[factor_name] = (low, high)
        factor_names.append(factor_name)
    
    # Parse response data
    responses = []
    for i in range(response_idx + 1, len(lines)):
        if lines[i]:
            response_values = [float(x) for x in lines[i].split(',')]
            responses.extend(response_values)
    
    return factors, factor_names, responses

def generate_design_matrix(factors, factor_names):
    # Generate all combinations of low/high for each factor
    levels = []
    for name in factor_names:
        low, high = factors[name]
        levels.append([low, high])
    
    design_matrix = []
    for combination in product(*levels):
        design_matrix.append(list(combination))
    
    return design_matrix

def calculate_effects(design_matrix, factor_names, responses):
    n_runs = len(design_matrix)
    n_factors = len(factor_names)
    
    # Convert design matrix to coded values (-1, +1)
    coded_matrix = []
    factor_ranges = {}
    
    for i, name in enumerate(factor_names):
        low_val = min(row[i] for row in design_matrix)
        high_val = max(row[i] for row in design_matrix)
        factor_ranges[name] = (low_val, high_val)
    
    for row in design_matrix:
        coded_row = []
        for i, val in enumerate(row):
            name = factor_names[i]
            low_val, high_val = factor_ranges[name]
            if val == low_val:
                coded_row.append(-1)
            else:
                coded_row.append(1)
        coded_matrix.append(coded_row)
    
    # Calculate main effects
    main_effects = {}
    for i, name in enumerate(factor_names):
        high_sum = sum(responses[j] for j in range(n_runs) if coded_matrix[j][i] == 1)
        low_sum = sum(responses[j] for j in range(n_runs) if coded_matrix[j][i] == -1)
        high_count = sum(1 for j in range(n_runs) if coded_matrix[j][i] == 1)
        low_count = sum(1 for j in range(n_runs) if coded_matrix[j][i] == -1)
        
        effect = (high_sum / high_count) - (low_sum / low_count)
        main_effects[name] = effect
    
    # Calculate interaction effects
    interactions = {}
    if n_factors >= 2:
        for i in range(n_factors):
            for j in range(i + 1, n_factors):
                name1 = factor_names[i]
                name2 = factor_names[j]
                
                interaction_sum = 0
                for k in range(n_runs):
                    interaction_sum += responses[k] * coded_matrix[k][i] * coded_matrix[k][j]
                
                interaction_effect = interaction_sum / n_runs
                interactions[f"{name1}{name2}"] = interaction_effect
    
    return main_effects, interactions

def main():
    factors, factor_names, responses = read_input()
    design_matrix = generate_design_matrix(factors, factor_names)
    main_effects, interactions = calculate_effects(design_matrix, factor_names, responses)
    
    # Sort factors by effect magnitude for significance ranking
    significant_factors = sorted(factor_names, key=lambda x: abs(main_effects[x]), reverse=True)
    
    # Build output
    result = {
        "main_effects": main_effects,
        "significant_factors": significant_factors
    }
    
    # Add interactions to result
    for interaction_name, effect in interactions.items():
        result[f"interaction_{interaction_name}"] = effect
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()