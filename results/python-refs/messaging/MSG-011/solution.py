import sys

def parse_length_prefixed_messages(hex_string):
    # Convert hex string to bytes
    data = bytes.fromhex(hex_string)
    
    messages = []
    offset = 0
    
    while offset < len(data):
        # Check if we have at least 4 bytes for length prefix
        if offset + 4 > len(data):
            break
            
        # Read 4-byte length prefix (big-endian)
        length = int.from_bytes(data[offset:offset+4], byteorder='big')
        offset += 4
        
        # Check if we have enough bytes for the message
        if offset + length > len(data):
            break
            
        # Extract the message
        message_bytes = data[offset:offset+length]
        message = message_bytes.decode('utf-8')
        messages.append(message)
        offset += length
    
    return messages

# Read input from stdin
hex_input = sys.stdin.read().strip()

# Parse messages and output
messages = parse_length_prefixed_messages(hex_input)
for message in messages:
    print(message)