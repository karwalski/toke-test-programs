import sys
import time
import hmac
import hashlib
import base64

def base32_decode(s):
    # Simple base32 decoder
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    s = s.upper().rstrip('=')
    
    # Convert to binary
    binary = ""
    for char in s:
        if char in alphabet:
            binary += format(alphabet.index(char), '05b')
    
    # Convert binary to bytes
    result = bytearray()
    for i in range(0, len(binary) - 4, 8):
        if i + 8 <= len(binary):
            byte_val = int(binary[i:i+8], 2)
            result.append(byte_val)
    
    return bytes(result)

def generate_totp(secret, timestamp=None):
    if timestamp is None:
        timestamp = int(time.time())
    
    # TOTP uses 30-second intervals
    counter = timestamp // 30
    
    # Convert counter to 8-byte big-endian
    counter_bytes = counter.to_bytes(8, 'big')
    
    # Decode base32 secret
    key = base32_decode(secret)
    
    # HMAC-SHA1
    mac = hmac.new(key, counter_bytes, hashlib.sha1).digest()
    
    # Dynamic truncation
    offset = mac[-1] & 0x0f
    code = int.from_bytes(mac[offset:offset+4], 'big') & 0x7fffffff
    
    # 6-digit code
    totp_code = code % 1000000
    
    return f"{totp_code:06d}"

def get_seconds_remaining():
    return 30 - (int(time.time()) % 30)

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

secret = lines[0]
command = lines[1]

if command == "generate":
    print("Code:")
elif command == "validate":
    provided_code = lines[2]
    
    # Check current and adjacent time windows
    current_time = int(time.time())
    valid = False
    
    for offset in [-1, 0, 1]:  # Allow 1 window tolerance
        test_time = current_time + (offset * 30)
        expected_code = generate_totp(secret, test_time)
        if provided_code == expected_code:
            valid = True
            break
    
    print("VALID" if valid else "INVALID")