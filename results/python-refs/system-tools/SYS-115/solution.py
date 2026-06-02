import sys
import os
import tempfile

# Read all input
lines = sys.stdin.read().splitlines()

# First line is the destination file path
dest_path = lines[0]

# Remaining lines are the content to write
content_lines = lines[1:]
content = '\n'.join(content_lines)

# Create temp file in the same directory as destination
dest_dir = os.path.dirname(dest_path) or '.'
with tempfile.NamedTemporaryFile(mode='w', dir=dest_dir, delete=False) as temp_file:
    temp_path = temp_file.name
    temp_file.write(content)

# Atomically move temp file to destination
os.rename(temp_path, dest_path)

# Output the result
byte_count = len(content.encode('utf-8'))
print(f"Written {byte_count} bytes to {dest_path} (atomically)")