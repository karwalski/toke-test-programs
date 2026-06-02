import sys

lines = sys.stdin.read().strip().split('\n')
max_possible_score = int(lines[0])

for i in range(1, len(lines)):
    raw_score = int(lines[i])
    normalized_score = (raw_score / max_possible_score) * 100
    print(f"{normalized_score:.1f}")