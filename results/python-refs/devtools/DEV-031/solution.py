import os
import sys

# Read the base directory from the first line
base_dir = input().strip()

# Process each remaining line
for line in sys.stdin:
    path = line.strip()
    if not path:
        continue
    
    # Join the base directory with the relative path
    full_path = os.path.join(base_dir, path)
    
    # Normalize the path to resolve . and .. components
    resolved_path = os.path.normpath(full_path)
    
    print(resolved_path)