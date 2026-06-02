import sys

for line in sys.stdin:
    line = line.strip()
    if line == line[::-1]:
        print(f"{line}: YES")
    else:
        print(f"{line}: NO")