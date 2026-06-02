import fnmatch
import sys

lines = []
for line in sys.stdin:
    lines.append(line.strip())

pattern = lines[0]
paths = lines[1:]

match_count = 0
total_count = len(paths)

for path in paths:
    if fnmatch.fnmatch(path, pattern):
        print(f"MATCH: {path}")
        match_count += 1
    else:
        print(f"NO MATCH: {path}")

print(f"{match_count}/{total_count} matched")