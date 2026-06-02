# Read input
numbers = list(map(int, input().split()))

# Initialize counters
comparisons = 0
swaps = 0

# Bubble sort with counting
n = len(numbers)
for i in range(n):
    for j in range(0, n - i - 1):
        comparisons += 1
        if numbers[j] > numbers[j + 1]:
            # Swap elements
            numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
            swaps += 1

# Output results
print("Sorted:", " ".join(map(str, numbers)))
print("Comparisons:", comparisons)
print("Swaps:", swaps)