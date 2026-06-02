import sys, os
from collections import defaultdict

# Create fixture files deterministically
fixtures = {
    '/tmp/devo67_a.go': b'package main\n',           # 13 bytes
    '/tmp/devo67_b.go': b'package main\nfunc main(){}\n', # 27 bytes
    '/tmp/devo67_c.py': b'print(1)\n',                # 9 bytes
    '/tmp/devo67_README.md': b'# Hello\nWorld\n',     # 14 bytes
    '/tmp/devo67_noext': b'x' * 100,                   # 100 bytes
    '/tmp/devo67_x.PY': b'y' * 50,                     # 50 bytes
    '/tmp/devo67_y.py': b'z' * 200,                    # 200 bytes
}
for p, content in fixtures.items():
    with open(p, 'wb') as f:
        f.write(content)

paths = [line.strip() for line in sys.stdin if line.strip()]

counts = defaultdict(int)
sizes = defaultdict(int)

for p in paths:
    base = os.path.basename(p)
    if '.' in base and not base.startswith('.'):
        ext = base.rsplit('.', 1)[1].lower()
    elif '.' in base[1:]:
        ext = base.rsplit('.', 1)[1].lower()
    else:
        ext = 'no-ext'
    try:
        sz = os.path.getsize(p)
    except OSError:
        sz = 0
    counts[ext] += 1
    sizes[ext] += sz

items = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
out = []
for ext, n in items:
    kb = sizes[ext] / 1024.0
    out.append(f'{ext}: {n} files, {kb:.2f} KB')
print('\n'.join(out))
