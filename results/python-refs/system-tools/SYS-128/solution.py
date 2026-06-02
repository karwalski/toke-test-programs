import sys

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

input_file = lines[0]
output_file = lines[1]
patches = lines[2:]

# Read input file
if input_file == '-':
    data = bytearray(sys.stdin.buffer.read())
else:
    with open(input_file, 'rb') as f:
        data = bytearray(f.read())

# Apply patches
total_bytes_patched = 0
num_offsets = len(patches)

for patch in patches:
    offset_str, hex_bytes = patch.split(':', 1)
    offset = int(offset_str)
    patch_bytes = bytes.fromhex(hex_bytes)
    
    # Apply the patch
    for i, byte_val in enumerate(patch_bytes):
        if offset + i < len(data):
            data[offset + i] = byte_val
        else:
            # Extend data if needed
            data.extend([0] * (offset + i - len(data) + 1))
            data[offset + i] = byte_val
    
    total_bytes_patched += len(patch_bytes)

# Write output file
if output_file == '-':
    sys.stdout.buffer.write(data)
    output_path = "stdout"
else:
    with open(output_file, 'wb') as f:
        f.write(data)
    output_path = output_file

# Print result
print(f"Patched {total_bytes_patched} bytes at {num_offsets} offsets. Output written to {output_path}.")