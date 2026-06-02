# Read input
numbers = list(map(int, input().split()))

# Find the maximum value to determine the range
max_val = max(numbers)

# Create count array
count = [0] * (max_val + 1)

# Count occurrences
for num in numbers:
    count[num] += 1

# Output count array (only non-zero counts)
count_parts = []
for i in range(len(count)):
    if count[i] > 0:
        count_parts.append(f"{i}:{count[i]}")

print("Counts:", " ".join(count_parts))

# Generate sorted result
sorted_result = []
for i in range(len(count)):
    if count[i] > 0:
        sorted_result.extend([i] * count[i])

print("Sorted:", " ".join(map(str, sorted_result)))