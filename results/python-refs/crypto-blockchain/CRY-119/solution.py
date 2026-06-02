import json
import sys

def rlp_encode(data):
    if isinstance(data, str):
        # Convert hex string to bytes
        if data.startswith('0x'):
            data = data[2:]
        try:
            byte_data = bytes.fromhex(data)
        except ValueError:
            # If not hex, treat as UTF-8 string
            byte_data = data.encode('utf-8')
        
        if len(byte_data) == 1 and byte_data[0] < 0x80:
            return byte_data
        elif len(byte_data) <= 55:
            return bytes([0x80 + len(byte_data)]) + byte_data
        else:
            length_bytes = len(byte_data).to_bytes((len(byte_data).bit_length() + 7) // 8, 'big')
            return bytes([0xb7 + len(length_bytes)]) + length_bytes + byte_data
    
    elif isinstance(data, list):
        # Encode each item in the list
        encoded_items = b''.join(rlp_encode(item) for item in data)
        
        if len(encoded_items) <= 55:
            return bytes([0xc0 + len(encoded_items)]) + encoded_items
        else:
            length_bytes = len(encoded_items).to_bytes((len(encoded_items).bit_length() + 7) // 8, 'big')
            return bytes([0xf7 + len(length_bytes)]) + length_bytes + encoded_items

# Read input from stdin
input_data = sys.stdin.read().strip()
data = json.loads(input_data)

# Encode and output as hex
result = rlp_encode(data)
print(result.hex())