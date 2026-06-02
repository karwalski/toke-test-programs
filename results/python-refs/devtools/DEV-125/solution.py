import json
import sys

def calculate_debt(file_data):
    """Calculate technical debt in hours for a single file"""
    complexity = file_data['complexity']
    duplication_pct = file_data['duplication_pct']
    coverage_pct = file_data['coverage_pct']
    age_days = file_data['age_days']
    
    # Base debt from complexity (exponential growth after threshold)
    if complexity <= 10:
        complexity_debt = complexity * 0.1
    else:
        complexity_debt = 1.0 + (complexity - 10) * 0.2
    
    # Duplication penalty (linear)
    duplication_debt = duplication_pct * 0.05
    
    # Coverage penalty (inverse relationship)
    coverage_debt = max(0, (100 - coverage_pct) * 0.03)
    
    # Age factor (logarithmic growth)
    import math
    age_factor = 1.0 + math.log(max(1, age_days / 365))
    
    # Total debt calculation
    total_debt = (complexity_debt + duplication_debt + coverage_debt) * age_factor
    
    return total_debt

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    files = json.loads(input_data)
    
    total_debt = 0.0
    
    # Process each file
    for file_data in files:
        file_name = file_data['file']
        debt = calculate_debt(file_data)
        total_debt += debt
        
        # Format and print file debt
        print(f"{file_name}: {debt:.1f}h")
    
    # Print total debt
    print(f"Total: {total_debt:.1f}h")

if __name__ == "__main__":
    main()