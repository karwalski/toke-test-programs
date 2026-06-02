import sys
from datetime import datetime

# Read input and process
file_changes = {}
file_last_changed = {}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split(' ', 1)
    date = parts[0]
    file_path = parts[1]
    
    # Count changes
    if file_path in file_changes:
        file_changes[file_path] += 1
    else:
        file_changes[file_path] = 1
    
    # Track last changed date
    if file_path not in file_last_changed:
        file_last_changed[file_path] = date
    else:
        # Compare dates and keep the latest
        if date > file_last_changed[file_path]:
            file_last_changed[file_path] = date

# Sort by change count descending
sorted_files = sorted(file_changes.items(), key=lambda x: x[1], reverse=True)

# Output results
for file_path, change_count in sorted_files:
    last_date = file_last_changed[file_path]
    print(f"{file_path}: {change_count} changes (last changed {last_date})")