import sys

lines = sys.stdin.read().splitlines()
spaces_per_tab = int(lines[0])

for line in lines[1:]:
    normalized_line = line.expandtabs(spaces_per_tab)
    print(normalized_line)