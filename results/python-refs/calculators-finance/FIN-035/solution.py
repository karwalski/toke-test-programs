import sys

# Conversion factors to grams
conversions = {
    'mg': 0.001,
    'g': 1.0,
    'kg': 1000.0,
    'tonne': 1000000.0,
    'oz': 28.3495,
    'lb': 453.592,
    'stone': 6350.29
}

line = input().strip()
parts = line.split()
value = float(parts[0])
source_unit = parts[1]
target_unit = parts[2]

# Convert to grams first, then to target unit
grams = value * conversions[source_unit]
result = grams / conversions[target_unit]

print(f"{result:.4f}")