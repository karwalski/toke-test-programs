import sys
import hmac
import hashlib
import base64
import time

def verify_jwt(token, secret):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return False
        
        header_payload = parts[0] + '.' + parts[1]
        signature = parts[2]
        
        # Add padding if needed for base64 decoding
        signature += '=' * (4 - len(signature) % 4)
        
        # Calculate expected signature
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            header_payload.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        # Encode to base64 and remove padding
        expected_signature_b64 = base64.urlsafe_b64encode(expected_signature).decode('utf-8').rstrip('=')
        
        return signature.rstrip('=') == expected_signature_b64
    except:
        return False

# Read input
jwt_token = input().strip()
wordlist_path = input().strip()

# Read wordlist
try:
    with open(wordlist_path, 'r') as f:
        words = [line.strip() for line in f if line.strip()]
except:
    print("Error reading wordlist file")
    sys.exit(1)

total = len(words)
start_time = time.time()
found = False

for i, word in enumerate(words, 1):
    print(f"Trying {i}/{total}")
    
    if verify_jwt(jwt_token, word):
        print(f"SECRET FOUND: {word}")
        found = True
        break

if not found:
    elapsed = time.time() - start_time
    print(f"Not found after {total} attempts in {elapsed:.0f}s")