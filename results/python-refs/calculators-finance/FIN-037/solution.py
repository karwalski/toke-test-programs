import sys

def convert_pressure(value, source_unit, target_unit):
    # Convert everything to Pa first, then to target unit
    
    # Conversion factors to Pa
    to_pa = {
        'Pa': 1,
        'kPa': 1000,
        'bar': 100000,
        'atm': 101325,
        'psi': 6894.75729,
        'mmHg': 133.322387415
    }
    
    # Convert to Pa
    pa_value = value * to_pa[source_unit]
    
    # Convert from Pa to target unit
    result = pa_value / to_pa[target_unit]
    
    return result

# Read input
line = input().strip()
parts = line.split()
value = float(parts[0])
source_unit = parts[1]
target_unit = parts[2]

# Convert and output
result = convert_pressure(value, source_unit, target_unit)
print(f"{result:.4f}")