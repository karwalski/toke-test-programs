import sys

def main():
    line = input().strip()
    parts = line.split()
    value = float(parts[0])
    source_unit = parts[1]
    target_unit = parts[2]
    convention = parts[3]
    
    # Define conversion factors
    if convention == "binary":
        base = 1024
    else:  # si
        base = 1000
    
    # Define unit hierarchy (from smallest to largest)
    units = ["bits", "bytes", "KB", "MB", "GB", "TB"]
    
    # Convert source to bits first
    source_idx = units.index(source_unit)
    if source_idx == 0:  # bits
        bits = value
    elif source_idx == 1:  # bytes
        bits = value * 8
    else:  # KB, MB, GB, TB
        bytes_val = value * (base ** (source_idx - 1))
        bits = bytes_val * 8
    
    # Convert bits to target unit
    target_idx = units.index(target_unit)
    if target_idx == 0:  # bits
        result = bits
    elif target_idx == 1:  # bytes
        result = bits / 8
    else:  # KB, MB, GB, TB
        bytes_val = bits / 8
        result = bytes_val / (base ** (target_idx - 1))
    
    print(f"{result:.4f}")

if __name__ == "__main__":
    main()