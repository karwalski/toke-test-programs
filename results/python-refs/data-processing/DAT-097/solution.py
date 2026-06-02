import sys

def detect_encoding(byte_data):
    # Try ASCII first (most restrictive)
    try:
        byte_data.decode('ascii')
        return 'ASCII'
    except UnicodeDecodeError:
        pass
    
    # Try UTF-8 next
    try:
        byte_data.decode('utf-8')
        return 'UTF-8'
    except UnicodeDecodeError:
        pass
    
    # Fall back to Latin-1 (can decode any byte sequence)
    return 'Latin-1'

# Read input
lines = sys.stdin.read().strip().split('\n')
encoding_hint = lines[0]
hex_string = lines[1]

# Convert hex string to bytes
byte_data = bytes.fromhex(hex_string)

# Detect or use provided encoding
if encoding_hint == 'detect':
    detected_encoding = detect_encoding(byte_data)
else:
    detected_encoding = encoding_hint

# Convert to UTF-8
if detected_encoding == 'ASCII':
    text = byte_data.decode('ascii')
elif detected_encoding == 'UTF-8':
    text = byte_data.decode('utf-8')
elif detected_encoding == 'Latin-1':
    text = byte_data.decode('latin-1')

# Output
if encoding_hint == 'detect':
    print(f"Detected: {detected_encoding}")
else:
    print(f"Detected: {detected_encoding}")
print(text)