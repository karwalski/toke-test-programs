import json
import sys

def encode_varint(value):
    """Encode an integer as a varint."""
    if value == 0:
        return bytes([0])
    
    result = []
    while value > 0:
        byte = value & 0x7F
        value >>= 7
        if value > 0:
            byte |= 0x80
        result.append(byte)
    return bytes(result)

def encode_string(value):
    """Encode a string as length-delimited bytes."""
    utf8_bytes = value.encode('utf-8')
    length = encode_varint(len(utf8_bytes))
    return length + utf8_bytes

def encode_field(tag, wire_type, data):
    """Encode a field with tag and wire type."""
    key = (tag << 3) | wire_type
    key_bytes = encode_varint(key)
    return key_bytes + data

def serialize_message(schema, data):
    """Serialize data according to schema."""
    fields_map = {field['name']: field for field in schema['fields']}
    result = b''
    annotations = []
    
    # Sort by tag number to ensure consistent output
    sorted_fields = sorted(schema['fields'], key=lambda x: x['tag'])
    
    for field in sorted_fields:
        name = field['name']
        tag = field['tag']
        field_type = field['type']
        
        if name not in data:
            continue
            
        value = data[name]
        
        if field_type == 'string':
            wire_type = 2  # Length-delimited
            encoded_data = encode_string(value)
            field_bytes = encode_field(tag, wire_type, encoded_data)
            annotations.append(f"field {tag} (string): {value}")
            
        elif field_type == 'int':
            wire_type = 0  # Varint
            encoded_data = encode_varint(value)
            field_bytes = encode_field(tag, wire_type, encoded_data)
            annotations.append(f"field {tag} (varint): {value}")
            
        elif field_type == 'bool':
            wire_type = 0  # Varint
            encoded_data = encode_varint(1 if value else 0)
            field_bytes = encode_field(tag, wire_type, encoded_data)
            annotations.append(f"field {tag} (varint): {1 if value else 0}")
            
        result += field_bytes
    
    return result, annotations

def main():
    lines = sys.stdin.read().strip().split('\n')
    schema = json.loads(lines[0])
    data = json.loads(lines[1])
    
    serialized_bytes, annotations = serialize_message(schema, data)
    
    # Convert to hex with spaces
    hex_output = ' '.join(f'{b:02x}' for b in serialized_bytes)
    print(hex_output)
    
    # Print annotations
    for annotation in annotations:
        print(annotation)

if __name__ == "__main__":
    main()