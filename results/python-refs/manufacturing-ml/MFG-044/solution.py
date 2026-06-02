import csv
import json
import sys
import math

def calculate_sigma_level(dpo):
    # Sigma level calculation using inverse normal distribution approximation
    # For DPO values, we need to find the Z-score that corresponds to the yield
    yield_rate = 1 - dpo
    
    # Handle edge cases
    if yield_rate >= 0.9999999:
        return 6.0
    if yield_rate <= 0.0000001:
        return 0.0
    
    # Inverse normal distribution approximation (Beasley-Springer-Moro algorithm)
    def inv_norm(p):
        if p <= 0 or p >= 1:
            return 0
        
        # Convert to standard normal (mean=0, std=1)
        # Use rational approximation for inverse normal
        c = [2.515517, 0.802853, 0.010328]
        d = [1.432788, 0.189269, 0.001308]
        
        if p > 0.5:
            # Use upper tail
            t = math.sqrt(-2 * math.log(1 - p))
            z = t - (c[0] + c[1]*t + c[2]*t*t) / (1 + d[0]*t + d[1]*t*t + d[2]*t*t*t)
        else:
            # Use lower tail
            t = math.sqrt(-2 * math.log(p))
            z = -t + (c[0] + c[1]*t + c[2]*t*t) / (1 + d[0]*t + d[1]*t*t + d[2]*t*t*t)
        
        return z
    
    z_score = inv_norm(yield_rate)
    # Add 1.5 sigma shift (standard Six Sigma practice)
    sigma_level = z_score + 1.5
    
    return max(0, sigma_level)

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
for row in reader:
    units = int(row['units'])
    defects = int(row['defects'])
    opportunities = int(row['opportunities'])
    
    # Calculate DPO (Defects Per Opportunity)
    total_opportunities = units * opportunities
    dpo = defects / total_opportunities
    
    # Calculate DPMO (Defects Per Million Opportunities)
    dpmo = dpo * 1000000
    
    # Calculate sigma level
    sigma_level = calculate_sigma_level(dpo)
    
    # Calculate yield percentage
    yield_percent = (1 - dpo) * 100
    
    # Format output
    result = {
        "dpo": round(dpo, 3),
        "dpmo": int(dpmo),
        "sigma_level": round(sigma_level, 2),
        "yield_percent": round(yield_percent, 1)
    }
    
    print(json.dumps(result, separators=(',', ':')))