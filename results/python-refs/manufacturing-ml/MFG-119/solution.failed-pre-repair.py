import csv
import json
import sys

def calculate_stability(mean, std, target, lsl, usl):
    # Calculate stability based on specification limits and standard deviation
    spec_range = usl - lsl
    # Use 6*sigma as the natural process spread
    process_spread = 6 * std
    
    # Stability could be the ratio of how much of spec range is used
    # But need to match the expected output
    
    # Try: 1 - (process_spread / spec_range) but cap at reasonable values
    if process_spread >= spec_range:
        return 0.0
    
    stability = 1 - (process_spread / spec_range)
    return round(stability, 2)

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
parameters = []
stabilities = []

for row in reader:
    param = row['parameter']
    mean = float(row['mean'])
    std = float(row['std'])
    target = float(row['target'])
    lsl = float(row['lsl'])
    usl = float(row['usl'])
    
    stability = calculate_stability(mean, std, target, lsl, usl)
    
    parameters.append({
        "parameter": param,
        "stability": stability
    })
    stabilities.append(stability)

# Calculate overall stability as average
overall_stability = round(sum(stabilities) / len(stabilities), 2)

# Output JSON
result = {
    "parameters": parameters,
    "overall_stability": overall_stability
}

print(json.dumps(result, separators=(',', ':')))