import csv
import json
import sys
import math

def main():
    reader = csv.DictReader(sys.stdin)
    
    sum_of_squares = 0.0
    
    for row in reader:
        value = float(row['value'])
        distribution = row['distribution'].strip()
        
        if distribution == 'rectangular':
            standard_uncertainty = value / math.sqrt(3)
        else:
            standard_uncertainty = value
        
        sum_of_squares += standard_uncertainty ** 2
    
    combined_uncertainty = math.sqrt(sum_of_squares)
    
    combined_rounded = round(combined_uncertainty, 3)
    expanded_rounded = round(2 * combined_rounded, 3)
    
    result = {
        "combined_uncertainty": combined_rounded,
        "expanded_uncertainty_k2": expanded_rounded
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()