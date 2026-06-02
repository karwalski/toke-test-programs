import sys, csv, json, math

def pearson(x, y):
    n = len(x)
    mx = sum(x)/n
    my = sum(y)/n
    num = sum((x[i]-mx)*(y[i]-my) for i in range(n))
    dx = math.sqrt(sum((x[i]-mx)**2 for i in range(n)))
    dy = math.sqrt(sum((y[i]-my)**2 for i in range(n)))
    if dx == 0 or dy == 0:
        return 0.0
    return num/(dx*dy)

def main():
    data = sys.stdin.read().strip().splitlines()
    reader = csv.reader(data)
    rows = list(reader)
    header = rows[0]
    body = [[float(v) for v in r] for r in rows[1:]]
    defect_idx = header.index('defect_rate')
    defects = [r[defect_idx] for r in body]
    cors = []
    for i, name in enumerate(header):
        if i == defect_idx:
            continue
        col = [r[i] for r in body]
        r = pearson(col, defects)
        cors.append({'variable': name, 'r': round(r, 2)})
    cors.sort(key=lambda x: abs(x['r']), reverse=True)
    out = {'correlations': cors, 'likely_root_cause': cors[0]['variable']}
    print(json.dumps(out))

main()
