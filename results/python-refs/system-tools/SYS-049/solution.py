import sys

lines = 0
words = 0
bytes_count = 0
max_line_length = 0

for line in sys.stdin:
    lines += 1
    bytes_count += len(line.encode('utf-8'))
    words += len(line.split())
    max_line_length = max(max_line_length, len(line.rstrip('\n\r')))

print(f"lines: {lines}  words: {words}  bytes: {bytes_count}  max_line: {max_line_length}")