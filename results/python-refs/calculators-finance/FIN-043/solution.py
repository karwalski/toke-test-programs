from collections import Counter

# Read input and parse numbers
numbers = list(map(int, input().split(',')))

# Count frequencies
counter = Counter(numbers)

# Find the maximum frequency
max_freq = max(counter.values())

# Find all numbers with maximum frequency (modes)
modes = [num for num, freq in counter.items() if freq == max_freq]

# Sort modes in ascending order and output
modes.sort()
print(','.join(map(str, modes)))