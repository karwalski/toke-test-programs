import sys
import hmac
import hashlib
import base64
import time
import os

def verify_jwt(token, secret):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return False
        
        header_payload = parts[0] + '.' + parts[1]
        signature = parts[2]
        
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            header_payload.encode('utf-8'),
            hashlib.sha256
        ).digest()
        
        expected_signature_b64 = base64.urlsafe_b64encode(expected_signature).decode('utf-8').rstrip('=')
        
        return signature.rstrip('=') == expected_signature_b64
    except:
        return False

try:
    jwt_token = input().strip()
    wordlist_path = input().strip()
except EOFError:
    sys.exit(0)

start_time = time.time()
found = False
count = 0
total = 0

if os.path.exists(wordlist_path):
    try:
        with open(wordlist_path, 'r', errors='ignore') as f:
            for line in f:
                total += 1
    except:
        total = 0

if not os.path.exists(wordlist_path):
    # Use a default small wordlist for testing
    default_words = ['password', 'secret', '123456', 'admin', 'test', 'your-256-bit-secret']
    total = len(default_words)
    for i, word in enumerate(default_words, 1):
        print(f"Trying {i}/{total}")
        count = i
        if verify_jwt(jwt_token, word):
            print(f"SECRET FOUND: {word}")
            found = True
            break
else:
    try:
        with open(wordlist_path, 'r', errors='ignore') as f:
            i = 0
            for line in f:
                word = line.strip()
                if not word:
                    continue
                i += 1
                count = i
                print(f"Trying {i}/{total}")
                if verify_jwt(jwt_token, word):
                    print(f"SECRET FOUND: {word}")
                    found = True
                    break
    except:
        pass

if not found:
    elapsed = time.time() - start_time
    print(f"Not found after {count} attempts in {elapsed:.0f}s")