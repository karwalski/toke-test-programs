import sys

def main():
    data_in = sys.stdin.read()
    lines = data_in.split('\n')
    file_path = lines[0].strip()
    max_bytes = int(lines[1].strip()) if len(lines) > 1 and lines[1].strip() else 0
    
    if file_path == '-':
        rest = '\n'.join(lines[2:])
        data = rest.encode()
    else:
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
        except FileNotFoundError:
            data = b''
    
    if max_bytes > 0:
        data = data[:max_bytes]
    
    if len(data) == 0:
        print('(empty)')
        return
    
    offset = 0
    out_lines = []
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        offset_str = f"{offset:08x}"
        
        hex_parts = []
        for j in range(0, len(chunk), 2):
            if j + 1 < len(chunk):
                hex_parts.append(f"{chunk[j]:02x}{chunk[j+1]:02x}")
            else:
                hex_parts.append(f"{chunk[j]:02x}")
        hex_str = " ".join(hex_parts)
        
        ascii_str = ""
        for byte in chunk:
            if 32 <= byte <= 126:
                ascii_str += chr(byte)
            else:
                ascii_str += "."
        
        out_lines.append(f"{offset_str}: {hex_str}  {ascii_str}")
        offset += len(chunk)
    
    print('\n'.join(out_lines))

if __name__ == "__main__":
    main()