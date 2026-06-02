import json
import sys

# Read input
config_line = input().strip()
message = input().strip()

# Parse config
config = json.loads(config_line)
header_bytes = config["header_bytes"]
encryption_block = config["encryption_block"]
frame_overhead = config["frame_overhead"]

# Calculate payload size
payload_size = len(message)

# Calculate padding needed for encryption block alignment
padding_needed = 0
if encryption_block > 0:
    remainder = payload_size % encryption_block
    if remainder != 0:
        padding_needed = encryption_block - remainder

# Calculate total size
total_size = payload_size + padding_needed + header_bytes + frame_overhead

# Calculate overhead percentage
overhead_percentage = ((total_size - payload_size) / total_size) * 100

# Output
print(f"payload: {payload_size} bytes")
print(f"padding: {padding_needed} bytes (to align to {encryption_block}-byte block)")
print(f"header: {header_bytes} bytes")
print(f"frame: {frame_overhead} bytes")
print(f"total: {total_size} bytes")
print(f"overhead: {overhead_percentage:.1f}%")