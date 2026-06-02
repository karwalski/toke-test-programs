import hashlib
import sys

def generate_idempotency_key(sender, recipient, content, timestamp):
    # Create the string to hash by joining with |
    message_string = f"{sender}|{recipient}|{content}|{timestamp}"
    
    # Generate SHA256 hash
    hash_object = hashlib.sha256(message_string.encode('utf-8'))
    hex_hash = hash_object.hexdigest()
    
    return hex_hash

def validate_key(key, stored_keys):
    if key in stored_keys:
        return "DUPLICATE"
    else:
        return "UNIQUE"

# Read input
operation = input().strip()

if operation == "generate":
    sender = input().strip()
    recipient = input().strip()
    content = input().strip()
    timestamp = input().strip()
    
    key = generate_idempotency_key(sender, recipient, content, timestamp)
    print(f"key: sha256({sender}|{recipient}|{content}|{timestamp}) = {key}")
    
elif operation == "validate":
    key = input().strip()
    stored_keys_input = input().strip()
    
    # Parse stored keys (assuming they're space-separated or comma-separated)
    if stored_keys_input:
        stored_keys = stored_keys_input.split()
    else:
        stored_keys = []
    
    result = validate_key(key, stored_keys)
    print(result)