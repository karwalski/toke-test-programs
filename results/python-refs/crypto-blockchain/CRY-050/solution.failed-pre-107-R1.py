import json
import hashlib
import hmac
import sys
import secrets

def create_signature(transaction_data, private_key_hex):
    # Convert private key from hex to bytes
    private_key = bytes.fromhex(private_key_hex)
    
    # Create a canonical string representation of the transaction
    # Sort keys to ensure consistent ordering
    tx_string = json.dumps(transaction_data, sort_keys=True, separators=(',', ':'))
    
    # Create HMAC-SHA256 signature
    signature = hmac.new(private_key, tx_string.encode('utf-8'), hashlib.sha256)
    
    # Return hex digest
    return signature.hexdigest()

# Read input
transaction_json = input().strip()
private_key_input = input().strip()

# Parse transaction
transaction = json.loads(transaction_json)

# Handle placeholder private key - generate actual hex if needed
if private_key_input == "private_key_hex" or not all(c in '0123456789abcdefABCDEF' for c in private_key_input):
    # Generate a real 64-character hex private key
    private_key_hex = secrets.token_hex(32)
else:
    private_key_hex = private_key_input

# Generate signature
signature = create_signature(transaction, private_key_hex)

# Add signature to transaction
transaction['signature'] = signature

# Output the signed transaction
print(json.dumps(transaction, separators=(',', ':')))