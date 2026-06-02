import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    samples = [float(x) for x in data[1:1+n]]
    if len(samples) != n:
        print('ERROR: sample count mismatch')
        return
    buckets = [0]*10
    for s in samples:
        if s < 0 or s > 100:
            print(f'ERROR: sample out of range: {s}')
            return
        idx = int(s // 10)
        if idx == 10:
            idx = 9
        buckets[idx] += 1
    parts = []
    for i in range(10):
        parts.append(f'{i*10}-{(i+1)*10}%: {buckets[i]}')
    print('CPU% histogram: ' + ', '.join(parts))

main()
