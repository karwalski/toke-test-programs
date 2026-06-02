import sys
import re

def parse_size(size_str):
    """Convert size string to bytes for comparison"""
    size_str = size_str.upper()
    if size_str.endswith('GB'):
        return float(size_str[:-2]) * 1024 * 1024 * 1024
    elif size_str.endswith('MB'):
        return float(size_str[:-2]) * 1024 * 1024
    elif size_str.endswith('KB'):
        return float(size_str[:-2]) * 1024
    elif size_str.endswith('B'):
        return float(size_str[:-1])
    else:
        # Assume bytes if no unit
        return float(size_str)

def format_size(size_bytes):
    """Convert bytes back to human readable format"""
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{int(size_bytes / (1024 * 1024 * 1024))}GB"
    elif size_bytes >= 1024 * 1024:
        return f"{int(size_bytes / (1024 * 1024))}MB"
    elif size_bytes >= 1024:
        return f"{int(size_bytes / 1024)}KB"
    else:
        return f"{int(size_bytes)}B"

layers = []
total_bytes = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    # Split on first space to separate size from command
    parts = line.split(' ', 1)
    if len(parts) >= 2:
        size_str = parts[0]
        command = parts[1]
        
        size_bytes = parse_size(size_str)
        total_bytes += size_bytes
        
        layers.append((size_bytes, size_str, command))

# Sort by size in descending order
layers.sort(key=lambda x: x[0], reverse=True)

# Output top 5 layers
for i, (size_bytes, original_size, command) in enumerate(layers[:5]):
    print(f"{i+1}. {original_size}: {command}")

# Output total
print(f"Total: {format_size(total_bytes)}")