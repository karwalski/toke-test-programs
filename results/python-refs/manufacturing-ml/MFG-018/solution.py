import csv
import sys
import json
import math

def calculate_sigma_level(dpmo):
    # Convert DPMO to yield
    yield_rate = 1 - (dpmo / 1000000)
    
    # Calculate Z-score using inverse normal distribution approximation
    # Using Beasley-Springer-Moro algorithm approximation
    if yield_rate >= 0.5:
        t = math.sqrt(-2 * math.log(1 - yield_rate))
        z = t - (2.515517 + 0.802853 * t + 0.010328 * t * t) / (1 + 1.432788 * t + 0.189269 * t * t + 0.001308 * t * t * t)
    else:
        t = math.sqrt(-2 * math.log(yield_rate))
        z = -(t - (2.515517 + 0.802853 * t + 0.010328 * t * t) / (1 + 1.432788 * t + 0.189269 * t * t + 0.001308 * t * t * t))
    
    # Sigma level is Z-score + 1.5 (shift)
    sigma_level = z + 1.5
    return sigma_level

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
for row in reader:
    units_produced = int(row['units_produced'])
    defects = int(row['defects'])
    opportunities_per_unit = int(row['opportunities_per_unit'])
    
    # Calculate total opportunities
    total_opportunities = units_produced * opportunities_per_unit
    
    # Calculate DPMO
    dpmo = (defects / total_opportunities) * 1000000
    
    # Calculate sigma level
    sigma_level = calculate_sigma_level(dpmo)
    
    # Format output
    result = {
        "dpmo": int(dpmo),
        "sigma_level": round(sigma_level, 2)
    }
    
    print(json.dumps(result, separators=(',', ':')))