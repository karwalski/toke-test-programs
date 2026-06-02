import json
import sys

data = json.loads(sys.stdin.read().strip())
data.sort()
n = len(data)

def pct(p):
    # nearest-rank-ish: index = ceil(p/100 * n) - 1
    import math
    k = math.ceil(p/100 * n) - 1
    if k < 0:
        k = 0
    return data[k]

slow = pct(25)
avg = pct(50)
fast = pct(75)

print(f"slow:{int(slow)} average:{int(avg)} fast:{int(fast)}")