# Read input
numbers = list(map(int, input().split()))

# Print initial state
print("Initial:", " ".join(map(str, numbers)))

# Bubble sort with output after each pass
n = len(numbers)
for i in range(n - 1):
    # Perform one pass of bubble sort
    swapped = False
    for j in range(n - 1 - i):
        if numbers[j] > numbers[j + 1]:
            numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
            swapped = True
    
    # Output state after this pass
    print(f"Pass {i + 1}:", " ".join(map(str, numbers)))
    
    # If no swaps occurred, the array is sorted
    if not swapped:
        break

# Print final sorted state
print("Sorted:", " ".join(map(str, numbers)))