import sys

lines = sys.stdin.read().strip().split('\n')
sort_option = lines[0].strip()
text_lines = lines[1:]

if sort_option == "yes":
    text_lines.sort()

seen = set()
result = []
for line in text_lines:
    if line not in seen:
        seen.add(line)
        result.append(line)

for line in result:
    print(line)