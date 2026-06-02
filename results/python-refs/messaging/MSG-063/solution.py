import json
import sys

def read_varint(data, pos):
    """Read a varint from data starting at pos, return (value, new_pos)"""
    result = 0
    shift = 0
    while pos < len(data):
        byte = data[pos]
        pos += 1
        result |= (byte & 0x7F) << shift
        if (byte & 0x80) == 0:
            break
        shift += 7
    return result, pos

def deserialize_binary(schema, binary_data):
    """Deserialize binary data according to schema"""
    # Build tag to field mapping
    tag_to_field = {}
    for field in schema['fields']:
        tag_to_field[field['tag']] = field
    
    result = {}
    pos = 0
    
    while pos < len(binary_data):
        # Read tag and wire type
        tag_wire, pos = read_varint(binary_data, pos)
        tag = tag_wire >> 3
        wire_type = tag_wire & 0x7
        
        if tag not in tag_to_field:
            # Skip unknown field
            if wire_type == 0:  # varint
                _, pos = read_varint(binary_data, pos)
            elif wire_type == 2:  # length-delimited
                length, pos = read_varint(binary_data, pos)
                pos += length
            continue
        
        field = tag_to_field[tag]
        field_name = field['name']
        field_type = field['type']
        
        if field_type == 'string':
            # Length-delimited (wire type 2)
            length, pos = read_varint(binary_data, pos)
            string_bytes = binary_data[pos:pos + length]
            result[field_name] = string_bytes.decode('utf-8')
            pos += length
        elif field_type == 'int':
            # Varint (wire type 0)
            value, pos = read_varint(binary_data, pos)
            result[field_name] = value
    
    return result

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    schema = json.loads(lines[0])
    hex_data = lines[1].replace(' ', '')
    
    # Convert hex to bytes
    binary_data = bytes.fromhex(hex_data)
    
    # Deserialize
    result = deserialize_binary(schema, binary_data)
    
    # Output as JSON (compact format to match expected output)
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()