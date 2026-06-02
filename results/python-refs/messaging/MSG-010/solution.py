import sys

for line in sys.stdin:
    message = line.rstrip('\n')
    message_bytes = message.encode('utf-8')
    length = len(message_bytes)
    
    # 4-byte big-endian length prefix
    length_bytes = length.to_bytes(4, 'big')
    
    # Convert to hex
    length_hex = length_bytes.hex()
    message_hex = message_bytes.hex()
    
    print(f"{length_hex}:{message_hex}")