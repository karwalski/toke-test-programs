import sys

def payback(inv, cfs):
    cum = 0.0
    for i, cf in enumerate(cfs):
        prev = cum
        cum += cf
        if cum >= inv:
            if cf == 0:
                return i + 1
            return i + (inv - prev) / cf
    return None

def main():
    data = sys.stdin.read().split('\n')
    first = data[0].split()
    inv = float(first[0]); r = float(first[1])
    cfs = [float(x) for x in data[1].split(',')]
    simple = payback(inv, cfs)
    dcfs = [cf / ((1 + r) ** (t + 1)) for t, cf in enumerate(cfs)]
    disc = payback(inv, dcfs)
    def fmt(v):
        return 'NEVER_RECOVERED' if v is None else f'{v:.2f}'
    print(fmt(simple))
    print(fmt(disc))

main()
