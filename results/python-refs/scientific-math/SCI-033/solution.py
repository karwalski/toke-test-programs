import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        print('Sorted: ')
        print('Gaps used: ')
        print('Comparisons: 0')
        return
    a = [int(x) for x in data]
    n = len(a)
    # Build Knuth gaps: h = 3h+1 while h < n/3 (Knuth uses h <= n/3 typically; standard: largest h with h < n/3)
    gaps = []
    h = 1
    while h < n:
        gaps.append(h)
        h = 3*h + 1
    # Use gaps in decreasing order, but only those satisfying Knuth condition h <= n/3 (actually standard is h < n)
    # Per spec: 'h = 3h+1 up to n/3'. For n=5, gaps up to floor(5/3)=1, so just [1]. But spec example shows '4 1'.
    # So interpretation: generate while h < n (i.e., h up to n-1 ish), then use in decreasing order.
    # For n=5: 1,4,13 -> stop at 13 (>=5). Used: 4,1. Matches.
    # For n=10: 1,4,13 -> stop. Used: 4,1. Matches.
    used_gaps = list(reversed(gaps))
    comparisons = 0
    for gap in used_gaps:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap:
                comparisons += 1
                if a[j-gap] > temp:
                    a[j] = a[j-gap]
                    j -= gap
                else:
                    break
            a[j] = temp
    print('Sorted: ' + ' '.join(str(x) for x in a))
    print('Gaps used: ' + ' '.join(str(g) for g in used_gaps))
    print('Comparisons: ' + str(comparisons))

main()
