from itertools import combinations

# Read input
elements = input().split()
k = int(input())

# Generate combinations
combos = list(combinations(elements, k))

# Output combinations
for combo in combos:
    print(' '.join(combo))

# Output total count
print(f"Total: {len(combos)}")