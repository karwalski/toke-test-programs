import sys
import json

def parse_tlv():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Find the blank line that separates type map from data
    blank_index = -1
    for i, line in enumerate(lines):
        if line == '':
            blank_index = i
            break
    
    # Parse type map
    type_map = {}
    for i in range(blank_index):
        parts = lines[i].split(' ', 1)
        type_id = int(parts[0], 16)
        type_name = parts[1]
        type_map[type_id] = type_name
    
    # Parse hex data
    hex_data = ''.join(lines[blank_index + 1:]).replace(' ', '')
    
    # Parse TLV data
    result = {}
    i = 0
    while i < len(hex_data):
        # Read type (1 byte)
        type_byte = int(hex_data[i:i+2], 16)
        i += 2
        
        # Read length (1 byte)
        length = int(hex_data[i:i+2], 16)
        i += 2
        
        # Read value (length bytes)
        value_hex = hex_data[i:i+length*2]
        i += length * 2
        
        # Convert hex to string
        value = bytes.fromhex(value_hex).decode('utf-8')
        
        # Check if it's a number (for age field)
        if type_map[type_byte] == 'age':
            value = int(value_hex, 16)
        
        result[type_map[type_byte]] = value
    
    print(json.dumps(result, separators=(',', ':')))

parse_tlv()