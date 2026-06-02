import sys
import json
import math
import csv
from io import StringIO

def calculate_sn_ratio(values, quality_type):
    """Calculate S/N ratio based on quality type"""
    n = len(values)
    
    if quality_type == "smaller":
        # Smaller-the-better: -10*log10(mean(y^2))
        sum_squares = sum(y**2 for y in values)
        mean_squares = sum_squares / n
        sn_ratio = -10 * math.log10(mean_squares)
    elif quality_type == "larger":
        # Larger-the-better: -10*log10(mean(1/y^2))
        sum_inv_squares = sum(1/(y**2) for y in values)
        mean_inv_squares = sum_inv_squares / n
        sn_ratio = -10 * math.log10(mean_inv_squares)
    elif quality_type == "nominal":
        # Nominal-the-best: 10*log10(mean^2/variance)
        mean_val = sum(values) / n
        variance = sum((y - mean_val)**2 for y in values) / (n - 1) if n > 1 else 0
        if variance == 0:
            sn_ratio = float('inf')
        else:
            sn_ratio = 10 * math.log10(mean_val**2 / variance)
    
    return round(sn_ratio, 1)

def main():
    input_text = sys.stdin.read().strip()
    lines = input_text.split('\n')
    
    quality_type = lines[0]
    
    # Parse CSV data
    csv_data = '\n'.join(lines[1:])
    csv_reader = csv.DictReader(StringIO(csv_data))
    
    # Organize data by factor and level
    data = {}
    for row in csv_reader:
        factor = row['factor']
        level = row['level']
        values = [float(x) for x in row['values'].split(';')]
        
        if factor not in data:
            data[factor] = {}
        data[factor][level] = values
    
    # Calculate S/N ratios
    sn_ratios = {}
    optimal = {}
    
    for factor in data:
        sn_ratios[factor] = {}
        best_sn = float('-inf')
        best_level = None
        
        for level in data[factor]:
            values = data[factor][level]
            sn_ratio = calculate_sn_ratio(values, quality_type)
            sn_ratios[factor][level] = sn_ratio
            
            if sn_ratio > best_sn:
                best_sn = sn_ratio
                best_level = level
        
        optimal[factor] = best_level
    
    # Output JSON
    result = {
        "sn_ratios": sn_ratios,
        "optimal": optimal
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()