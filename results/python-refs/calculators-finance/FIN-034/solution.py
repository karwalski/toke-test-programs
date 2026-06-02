import sys

def convert_length():
    line = input().strip()
    parts = line.split()
    value = float(parts[0])
    source_unit = parts[1]
    target_unit = parts[2]
    
    # Conversion factors to meters
    to_meters = {
        'mm': 0.001,
        'cm': 0.01,
        'm': 1.0,
        'km': 1000.0,
        'in': 0.0254,
        'ft': 0.3048,
        'yd': 0.9144,
        'mi': 1609.344
    }
    
    # Convert to meters first, then to target unit
    meters = value * to_meters[source_unit]
    result = meters / to_meters[target_unit]
    
    print(f"{result:.4f}")

convert_length()