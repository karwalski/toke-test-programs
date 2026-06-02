import sys

def main():
    data = sys.stdin.read().split()
    r = int(data[0], 16)
    s = int(data[1], 16)
    n = int(data[2], 16)
    half = n // 2
    if s <= half:
        print('CANONICAL')
    else:
        ns = n - s
        print('MALLEABLE (normalized s = {:x})'.format(ns))

main()
