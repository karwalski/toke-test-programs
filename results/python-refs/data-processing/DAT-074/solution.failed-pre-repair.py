import sys
import json

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Parse field definitions
    fields = []
    i = 0
    while i < len(lines) and lines[i].strip():
        parts = lines[i].strip().split()
        name = parts[0]
        offset_bits = int(parts[1])
        width_bits = int(parts[2])
        fields.append((name, offset_bits, width_bits))
        i += 1
    
    # Skip blank line
    i += 1
    
    # Process hex data lines
    while i < len(lines):
        hex_data = lines[i].strip()
        if hex_data:
            # Convert hex to binary
            binary_data = bin(int(hex_data, 16))[2:].zfill(len(hex_data) * 4)
            
            # Extract fields
            result = {}
            for name, offset_bits, width_bits in fields:
                field_bits = binary_data[offset_bits:offset_bits + width_bits]
                field_value = int(field_bits, 2)
                result[name] = field_value
            
            # Output JSON
            print(json.dumps(result, separators=(',', ':')))
        i += 1

if __name__ == "__main__":
    main()