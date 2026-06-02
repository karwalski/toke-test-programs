import sys

def main():
    # Read input
    file_path = input().strip()
    max_bytes = int(input().strip())
    
    # Read data
    if file_path == '-':
        # Read from stdin
        data = sys.stdin.buffer.read()
    else:
        # Read from file
        with open(file_path, 'rb') as f:
            data = f.read()
    
    # Limit bytes if specified
    if max_bytes > 0:
        data = data[:max_bytes]
    
    # Process data in 16-byte chunks
    offset = 0
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        
        # Format offset (8 hex digits)
        offset_str = f"{offset:08x}"
        
        # Format hex bytes in groups of 2
        hex_parts = []
        for j in range(0, len(chunk), 2):
            if j + 1 < len(chunk):
                hex_parts.append(f"{chunk[j]:02x}{chunk[j+1]:02x}")
            else:
                hex_parts.append(f"{chunk[j]:02x}")
        
        # Pad hex output to align ASCII
        hex_str = " ".join(hex_parts)
        if len(chunk) < 16:
            # Calculate padding needed
            remaining_bytes = 16 - len(chunk)
            if remaining_bytes % 2 == 1:
                # Odd number of remaining bytes
                hex_str += f"{chunk[-1]:02x}" if len(chunk) % 2 == 1 else ""
                hex_parts = hex_parts[:-1] if len(chunk) % 2 == 1 else hex_parts
                hex_str = " ".join(hex_parts)
                if len(chunk) % 2 == 1:
                    hex_str += f" {chunk[-1]:02x}"
        
        # Format ASCII representation
        ascii_str = ""
        for byte in chunk:
            if 32 <= byte <= 126:  # Printable ASCII
                ascii_str += chr(byte)
            else:
                ascii_str += "."
        
        # Output line
        print(f"{offset_str}: {hex_str}  {ascii_str}")
        
        offset += len(chunk)

if __name__ == "__main__":
    main()