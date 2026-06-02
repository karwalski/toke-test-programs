import sys, csv, json
data = sys.stdin.read()
lines = data.splitlines()
reader = csv.reader(lines)
rows = list(reader)
if not rows:
    print('[]')
else:
    header = rows[0]
    out = []
    for r in rows[1:]:
        d = {}
        for i, k in enumerate(header):
            d[k] = r[i] if i < len(r) else ''
        out.append(d)
    print(json.dumps(out, separators=(',', ':')))
