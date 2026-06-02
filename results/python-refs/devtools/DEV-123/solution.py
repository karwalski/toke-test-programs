import json
import sys

def format_bytes(bytes_val):
    if bytes_val >= 1024 * 1024:
        return f"{bytes_val / (1024 * 1024):.1f} MB"
    elif bytes_val >= 1024:
        return f"{bytes_val / 1024:.1f} KB"
    else:
        return f"{bytes_val} B"

# Read input from stdin
input_data = sys.stdin.read().strip()
allocations = json.loads(input_data)

# Sort by alloc_bytes descending
allocations.sort(key=lambda x: x['alloc_bytes'], reverse=True)

# Output top 10
for i, alloc in enumerate(allocations[:10], 1):
    function = alloc['function']
    file = alloc['file']
    line = alloc['line']
    alloc_bytes = alloc['alloc_bytes']
    alloc_count = alloc['alloc_count']
    
    formatted_bytes = format_bytes(alloc_bytes)
    
    print(f"{i}. {function} ({file}:{line})")
    print(f"   {formatted_bytes} in {alloc_count} allocs")