import sys
import json
import base64
import time

def decode_jwt_part(encoded_part):
    # Add padding if needed for base64 decoding
    padding = 4 - len(encoded_part) % 4
    if padding != 4:
        encoded_part += '=' * padding
    
    decoded_bytes = base64.urlsafe_b64decode(encoded_part)
    return json.loads(decoded_bytes.decode('utf-8'))

def main():
    jwt_token = sys.stdin.readline().strip()
    
    # Split JWT into parts
    parts = jwt_token.split('.')
    if len(parts) != 3:
        print("Invalid JWT format")
        return
    
    header_encoded, payload_encoded, signature_encoded = parts
    
    # Decode header and payload
    header = decode_jwt_part(header_encoded)
    payload = decode_jwt_part(payload_encoded)
    
    # Pretty print header and payload
    print(json.dumps(header, indent=2))
    print(json.dumps(payload, indent=2))
    
    # Check expiry
    current_time = int(time.time())
    
    if 'exp' in payload:
        exp_time = payload['exp']
        if current_time >= exp_time:
            print("Token expired")
        else:
            seconds_remaining = exp_time - current_time
            print(f"Expires in {seconds_remaining} seconds")
    else:
        # If no expiry field, we can't determine expiry status
        # The requirement doesn't specify what to do in this case
        pass

if __name__ == "__main__":
    main()