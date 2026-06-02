import json
import hashlib
import sys

def keccak256(data):
    """Simple Keccak-256 implementation using hashlib"""
    return hashlib.sha3_256(data).digest()

def rlp_encode(data):
    """Simple RLP encoding implementation"""
    if isinstance(data, int):
        if data == 0:
            return b''
        hex_str = hex(data)[2:]
        if len(hex_str) % 2:
            hex_str = '0' + hex_str
        return bytes.fromhex(hex_str)
    elif isinstance(data, str):
        if data.startswith('0x'):
            if len(data) == 2:  # Just "0x"
                return b''
            hex_str = data[2:]
            if len(hex_str) % 2:
                hex_str = '0' + hex_str
            # Check if hex_str contains only valid hex characters
            try:
                return bytes.fromhex(hex_str)
            except ValueError:
                # If not valid hex, treat as regular string
                return data.encode('utf-8')
        else:
            return data.encode('utf-8')
    elif isinstance(data, bytes):
        return data
    elif isinstance(data, list):
        encoded_items = []
        total_length = 0
        
        for item in data:
            encoded_item = rlp_encode(item)
            if len(encoded_item) == 0:
                encoded_items.append(b'\x80')
            elif len(encoded_item) == 1 and encoded_item[0] < 0x80:
                # Single byte less than 0x80
                encoded_items.append(encoded_item)
            elif len(encoded_item) <= 55:
                # Short string
                encoded_items.append(bytes([0x80 + len(encoded_item)]) + encoded_item)
            else:
                # Long string
                length_bytes = len(encoded_item).to_bytes((len(encoded_item).bit_length() + 7) // 8, 'big')
                encoded_items.append(bytes([0xb7 + len(length_bytes)]) + length_bytes + encoded_item)
            total_length += len(encoded_items[-1])
        
        # Combine all encoded items
        payload = b''.join(encoded_items)
        
        if total_length <= 55:
            return bytes([0xc0 + total_length]) + payload
        else:
            length_bytes = total_length.to_bytes((total_length.bit_length() + 7) // 8, 'big')
            return bytes([0xf7 + len(length_bytes)]) + length_bytes + payload
    
    return b''

def create_eip155_signing_hash(tx_data, chain_id):
    """Create EIP-155 signing hash for a transaction"""
    # Extract transaction fields
    nonce = tx_data.get('nonce', 0)
    gas_price = tx_data.get('gas_price', 0)
    gas_limit = tx_data.get('gas_limit', 21000)
    to = tx_data.get('to', '')
    value = tx_data.get('value', 0)
    data = tx_data.get('data', '')
    
    # Clean up the 'to' field - remove invalid hex characters
    if to.startswith('0x'):
        to_clean = '0x'
        hex_part = to[2:]
        for c in hex_part:
            if c in '0123456789abcdefABCDEF':
                to_clean += c
        to = to_clean
    
    # For EIP-155, append chain_id, 0, 0 to the transaction data
    rlp_array = [nonce, gas_price, gas_limit, to, value, data, chain_id, 0, 0]
    
    # RLP encode the array
    rlp_encoded = rlp_encode(rlp_array)
    
    # Get Keccak256 hash
    signing_hash = keccak256(rlp_encoded)
    
    return signing_hash.hex()

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

tx_json = lines[0]
chain_id = int(lines[1])

# Parse transaction JSON
tx_data = json.loads(tx_json)

# Create signing hash
signing_hash = create_eip155_signing_hash(tx_data, chain_id)
print(signing_hash)