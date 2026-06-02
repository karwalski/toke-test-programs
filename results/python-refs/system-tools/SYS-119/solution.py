import sys

data = sys.stdin.read()
parts = data.split('---\n', 1)
if len(parts) == 2:
    header, body = parts[0], parts[1]
else:
    header, body = '', parts[0]

filt = header.strip()

out = []
for line in body.splitlines():
    line = line.rstrip()
    if not line:
        continue
    fields = line.split()
    if len(fields) < 3:
        continue
    name = fields[0]
    try:
        size_bytes = int(fields[1])
        use_count = int(fields[2])
    except ValueError:
        continue
    if filt and filt not in name:
        continue
    size_kb = size_bytes // 1024
    out.append(f'{name} {size_kb} {use_count}')

print('\n'.join(out))
