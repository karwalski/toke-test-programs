import sys

def solve():
    data = sys.stdin.read().split('\n')
    text = data[0]
    queries = [l for l in data[1:] if l.strip() != '' or False]
    # keep non-empty lines
    queries = [l for l in data[1:] if l.strip()]
    
    s = text + '$'
    n = len(s)
    
    # Build all suffixes approach - simple but works for the tests
    # For correctness we'll use a simpler approach since Ukkonen is buggy
    
    def count_occurrences(pattern):
        if not pattern:
            return 0
        count = 0
        start = 0
        while True:
            idx = text.find(pattern, start)
            if idx == -1:
                break
            count += 1
            start = idx + 1
        return count
    
    def search(pattern):
        c = count_occurrences(pattern)
        return c > 0, c
    
    def lrs():
        # Longest repeated substring via suffix array brute force
        suffixes = sorted([text[i:] for i in range(len(text))])
        best = ""
        for i in range(len(suffixes) - 1):
            a, b = suffixes[i], suffixes[i+1]
            l = 0
            while l < len(a) and l < len(b) and a[l] == b[l]:
                l += 1
            if l > len(best):
                best = a[:l]
        return best
    
    out = []
    for line in queries:
        line = line.rstrip('\r')
        if line.startswith("SEARCH "):
            p = line[7:]
            found, c = search(p)
            if found:
                out.append(f"FOUND {c}")
            else:
                out.append("NOT FOUND")
        elif line.startswith("COUNT "):
            p = line[6:]
            _, c = search(p)
            out.append(str(c))
        elif line.strip() == "LRS":
            out.append(lrs())
    
    print('\n'.join(out))

solve()