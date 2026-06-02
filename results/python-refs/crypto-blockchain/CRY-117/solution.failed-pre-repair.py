import hashlib
import sys

def parse_function_signature(sig):
    """Parse function signature to extract function name and parameter types."""
    paren_idx = sig.index('(')
    func_name = sig[:paren_idx]
    params_str = sig[paren_idx+1:-1]
    
    if params_str.strip() == '':
        return func_name, []
    
    # Split parameters by comma
    params = [param.strip() for param in params_str.split(',')]
    return func_name, params

def encode_address(value):
    """Encode an address to 32 bytes (padded with zeros on the left)."""
    if value.startswith('0x'):
        value = value[2:]
    # Pad to 64 hex chars (32 bytes)
    return value.lower().zfill(64)

def encode_uint256(value):
    """Encode a uint256 to 32 bytes."""
    num = int(value)
    # Convert to 64 hex chars (32 bytes), big-endian
    return format(num, '064x')

def encode_parameter(param_type, value):
    """Encode a single parameter based on its type."""
    if param_type == 'address':
        return encode_address(value)
    elif param_type.startswith('uint'):
        return encode_uint256(value)
    else:
        raise ValueError(f"Unsupported parameter type: {param_type}")

def compute_function_selector(signature):
    """Compute the 4-byte function selector from the signature."""
    # Keccak-256 hash of the signature
    # Since we can't use external libraries, we'll use sha3_256 from hashlib
    hash_obj = hashlib.sha3_256(signature.encode('utf-8'))
    hash_bytes = hash_obj.digest()
    # Take first 4 bytes
    return hash_bytes[:4].hex()

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    signature = lines[0]
    args = lines[1:]
    
    # Parse function signature
    func_name, param_types = parse_function_signature(signature)
    
    # Compute function selector
    selector = compute_function_selector(signature)
    
    # Encode arguments
    encoded_args = []
    for i, param_type in enumerate(param_types):
        if i < len(args):
            encoded_arg = encode_parameter(param_type, args[i])
            encoded_args.append(encoded_arg)
    
    # Combine selector and encoded arguments
    result = selector + ''.join(encoded_args)
    print(result)

if __name__ == "__main__":
    main()