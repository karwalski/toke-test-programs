import sys

def convert_units():
    line = input().strip()
    parts = line.split()
    value = float(parts[0])
    source_unit = parts[1]
    target_unit = parts[2]
    
    # Conversion factors to liters
    to_liters = {
        'L': 1.0,
        'mL': 0.001,
        'gal_us': 3.785411784,
        'gal_uk': 4.54609,
        'cup': 0.236588,
        'fl_oz': 0.0295735
    }
    
    # Convert to liters first, then to target unit
    liters = value * to_liters[source_unit]
    result = liters / to_liters[target_unit]
    
    print(f"{result:.4f}")

convert_units()