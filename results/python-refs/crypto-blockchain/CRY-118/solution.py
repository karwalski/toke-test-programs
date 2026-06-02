import sys

def decode_abi_calldata(signature, calldata_hex):
    # Remove '0x' prefix if present
    if calldata_hex.startswith('0x'):
        calldata_hex = calldata_hex[2:]
    
    # Extract function selector (first 4 bytes = 8 hex chars)
    calldata_hex = calldata_hex[8:]
    
    # Parse function signature to get parameter types
    func_name = signature.split('(')[0]
    params_str = signature.split('(')[1].rstrip(')')
    
    if not params_str:
        return []
    
    param_types = [p.strip() for p in params_str.split(',')]
    
    # Convert hex to bytes
    calldata_bytes = bytes.fromhex(calldata_hex)
    
    results = []
    offset = 0
    
    for param_type in param_types:
        if param_type == 'address':
            # Address is 20 bytes, but padded to 32 bytes
            addr_bytes = calldata_bytes[offset + 12:offset + 32]
            addr_hex = '0x' + addr_bytes.hex()
            results.append(f"address: {addr_hex}")
            offset += 32
        elif param_type.startswith('uint'):
            # uint256 is 32 bytes
            uint_bytes = calldata_bytes[offset:offset + 32]
            uint_val = int.from_bytes(uint_bytes, byteorder='big')
            results.append(f"{param_type}: {uint_val}")
            offset += 32
    
    return results

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

signature = lines[0]
calldata = lines[1]

# Decode and output
results = decode_abi_calldata(signature, calldata)
for result in results:
    print(result)