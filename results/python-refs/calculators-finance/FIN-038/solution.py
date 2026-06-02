import sys

def main():
    line = input().strip()
    parts = line.split()
    value = float(parts[0])
    source_unit = parts[1]
    target_unit = parts[2]
    
    # Conversion factors to joules
    to_joules = {
        'J': 1.0,
        'cal': 4.184,
        'kWh': 3600000.0,
        'BTU': 1055.06,
        'eV': 1.602176634e-19
    }
    
    # Convert to joules first, then to target unit
    joules = value * to_joules[source_unit]
    result = joules / to_joules[target_unit]
    
    print(f"{result:.4f}")

if __name__ == "__main__":
    main()