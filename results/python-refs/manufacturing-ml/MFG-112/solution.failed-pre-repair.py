import csv
import json
import sys
import math

def main():
    # Read CSV from stdin
    reader = csv.DictReader(sys.stdin)
    
    sum_of_squares = 0.0
    
    for row in reader:
        value = float(row['value'])
        distribution = row['distribution'].strip()
        
        # Convert to standard uncertainty
        if distribution == 'rectangular':
            # For rectangular distribution, divide by sqrt(3)
            standard_uncertainty = value / math.sqrt(3)
        elif distribution == 'normal':
            # For normal distribution, value is already standard uncertainty
            standard_uncertainty = value
        else:
            # Default to normal if unknown
            standard_uncertainty = value
        
        # Add variance (square of standard uncertainty)
        sum_of_squares += standard_uncertainty ** 2
    
    # Combined uncertainty is square root of sum of variances
    combined_uncertainty = math.sqrt(sum_of_squares)
    
    # Expanded uncertainty with coverage factor k=2
    expanded_uncertainty_k2 = 2 * combined_uncertainty
    
    # Round to 3 decimal places
    combined_uncertainty = round(combined_uncertainty, 3)
    expanded_uncertainty_k2 = round(expanded_uncertainty_k2, 3)
    
    # Output JSON
    result = {
        "combined_uncertainty": combined_uncertainty,
        "expanded_uncertainty_k2": expanded_uncertainty_k2
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()