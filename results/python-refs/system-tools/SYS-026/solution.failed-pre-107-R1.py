import os
import re
import sys

# Read input
directory = input().strip()
pattern = input().strip()
replacement = input().strip()
dry_run = input().strip().lower() == 'yes'

# Get list of files in directory
try:
    files = os.listdir(directory)
except (OSError, FileNotFoundError):
    files = []

# Process each file
renamed_count = 0
rename_operations = []

for filename in files:
    old_path = os.path.join(directory, filename)
    
    # Skip if it's a directory
    if os.path.isdir(old_path):
        continue
    
    # Apply regex substitution
    new_filename = re.sub(pattern, replacement, filename)
    
    # Only proceed if the filename actually changed
    if new_filename != filename:
        new_path = os.path.join(directory, new_filename)
        rename_operations.append((filename, new_filename, old_path, new_path))

# Sort operations for consistent output
rename_operations.sort()

# Execute or simulate renames
for old_name, new_name, old_path, new_path in rename_operations:
    print(f"RENAME {old_name} -> {new_name}")
    
    if not dry_run:
        try:
            os.rename(old_path, new_path)
            renamed_count += 1
        except OSError:
            pass  # Skip files that can't be renamed
    else:
        renamed_count += 1

print(f"Summary: {renamed_count} files renamed.")