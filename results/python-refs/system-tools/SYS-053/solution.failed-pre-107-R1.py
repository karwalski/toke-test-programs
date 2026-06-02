import sys
import os

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

output_file = lines[0]
input_files = lines[1:]

total_bytes = 0
files_processed = 0

# Open output file for writing
with open(output_file, 'wb') as outf:
    # Read each input file and write to output
    for input_file in input_files:
        if os.path.exists(input_file):
            with open(input_file, 'rb') as inf:
                data = inf.read()
                outf.write(data)
                total_bytes += len(data)
                files_processed += 1

# Print result
print(f"Merged: {files_processed} files into {output_file}. Total: {total_bytes} bytes.")