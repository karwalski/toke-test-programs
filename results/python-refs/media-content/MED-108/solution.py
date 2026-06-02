import sys

unordered_count = 0
ordered_count = 0

for line in sys.stdin:
    line = line.strip()
    if line.startswith('- '):
        unordered_count += 1
    elif line and line[0].isdigit() and '. ' in line:
        ordered_count += 1

print(f"unordered: {unordered_count}")
print(f"ordered: {ordered_count}")