import sys

lines = sys.stdin.read().splitlines()
target_style = lines[0]

def is_hr(line):
    s = line.strip()
    if not s:
        return False
    for ch in ['-', '*', '_']:
        if all(c == ch for c in s):
            return True
        # spaced variant like - - -
        parts = s.split(' ')
        if len(parts) >= 3 and all(p == ch for p in parts):
            return True
    return False

out = []
# Include the first line as part of output (it's also the target style line per tests)
for i in range(0, len(lines)):
    line = lines[i]
    if is_hr(line):
        out.append(target_style)
    else:
        out.append(line)

print('\n'.join(out))