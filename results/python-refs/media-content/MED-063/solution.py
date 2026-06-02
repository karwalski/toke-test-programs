import sys

data = sys.stdin.read()
# Split keeping first line as target marker (2 chars)
newline_idx = data.find('\n')
if newline_idx == -1:
    target_marker = data
    rest = ''
else:
    target_marker = data[:newline_idx]
    rest = data[newline_idx+1:]

lines = rest.split('\n')
out = [target_marker]
for line in lines:
    i = 0
    while i < len(line) and line[i] in ' \t':
        i += 1
    if i < len(line) and line[i] in '-*+' and (i+1 >= len(line) or line[i+1] == ' '):
        if i+1 < len(line):
            new_line = line[:i] + target_marker + line[i+2:]
        else:
            new_line = line[:i] + target_marker.rstrip()
        out.append(new_line)
    else:
        out.append(line)

print('\n'.join(out))