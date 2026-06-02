import zipfile
import os
import sys

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

output_zip_path = lines[0]
input_paths = lines[1:]

# Create zip archive
entry_count = 0
with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for path in input_paths:
        if os.path.isfile(path):
            zipf.write(path, path)
            print(f"deflating: {path}")
            entry_count += 1
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, file_path)
                    print(f"deflating: {file_path}")
                    entry_count += 1

print(f"Archive: {output_zip_path} ({entry_count} entries)")