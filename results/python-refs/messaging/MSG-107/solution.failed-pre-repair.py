import sys
import json
import hashlib
import secrets
import datetime

def main():
    lines = sys.stdin.read().strip().split('\n')
    passes = int(lines[0])
    message_json = lines[1]
    
    # Parse the message to get the ID
    message = json.loads(message_json)
    message_id = message["id"]
    
    # Convert message to bytes for overwriting
    message_bytes = message_json.encode('utf-8')
    message_length = len(message_bytes)
    
    # Track the current data state
    current_data = bytearray(message_bytes)
    final_hash = None
    
    # Perform overwrite passes
    for pass_num in range(1, passes + 1):
        if pass_num == 2:
            # Pass 2: zero overwrite
            overwrite_data = bytearray(message_length)
            pattern_desc = "zero overwrite"
        else:
            # Pass 1 and 3+: random overwrite
            overwrite_data = bytearray(secrets.token_bytes(message_length))
            pattern_desc = "random overwrite"
        
        # Overwrite the data
        current_data[:] = overwrite_data
        
        # Calculate verification hash
        verification_hash = hashlib.sha256(current_data).hexdigest()
        
        # Output the pass result
        print(f"pass {pass_num}: {pattern_desc}, hash={verification_hash}")
        
        if pass_num == passes:
            final_hash = verification_hash
    
    # Generate deletion certificate
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    
    print(f"deletion certificate: {{id: {message_id}, passes: {passes}, final_hash: {final_hash}, timestamp: {timestamp}}}")

if __name__ == "__main__":
    main()