# Read input
line1 = input().split()
min_val = int(line1[0])
max_val = int(line1[1])

line2 = input().split()
numbers = [int(x) for x in line2]

# Create count array
count_range = max_val - min_val + 1
count = [0] * count_range

# Count occurrences
for num in numbers:
    if min_val <= num <= max_val:
        count[num - min_val] += 1

# Generate sorted array
sorted_numbers = []
for i in range(count_range):
    value = i + min_val
    sorted_numbers.extend([value] * count[i])

# Output results
print("Sorted:", " ".join(map(str, sorted_numbers)))
print("Count array:", " ".join(map(str, count)))