import sys

for line in sys.stdin:
    line = line.strip()
    if line:
        base_score, extra_credit, max_score = map(int, line.split())
        final_score = min(base_score + extra_credit, max_score)
        print(final_score)