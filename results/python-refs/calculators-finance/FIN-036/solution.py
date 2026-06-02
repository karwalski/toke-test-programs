import sys

def convert_speed(value, source_unit, target_unit):
    # Conversion factors to m/s
    to_ms = {
        'ms': 1.0,
        'kmh': 1/3.6,
        'mph': 0.44704,
        'knots': 0.514444,
        'mach': 343.0
    }
    
    # Conversion factors from m/s
    from_ms = {
        'ms': 1.0,
        'kmh': 3.6,
        'mph': 2.236936,
        'knots': 1.943844,
        'mach': 1/343.0
    }
    
    # Convert to m/s first, then to target unit
    ms_value = value * to_ms[source_unit]
    result = ms_value * from_ms[target_unit]
    
    return result

# Read input
line = input().strip()
parts = line.split()
value = float(parts[0])
source_unit = parts[1]
target_unit = parts[2]

# Convert and output
result = convert_speed(value, source_unit, target_unit)
print(f"{result:.4f}")