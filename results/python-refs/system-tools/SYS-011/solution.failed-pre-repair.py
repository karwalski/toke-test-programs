import os
import tarfile
import sys

# Read input
source_dir = input().strip()
output_path = input().strip()

# Create tar archive
file_count = 0
with tarfile.open(output_path, 'w') as tar:
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # Get the relative path for the archive
            arcname = os.path.relpath(file_path, source_dir)
            tar.add(file_path, arcname=arcname)
            print(f"added: {arcname}")
            file_count += 1

print(f"Archive created: {output_path} ({file_count} files)")