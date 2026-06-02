def insertion_sort_with_counts(arr):
    comparisons = 0
    shifts = 0
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Count comparison and move elements greater than key
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                shifts += 1
                j -= 1
            else:
                break
        
        # Place key in correct position
        if j + 1 != i:
            arr[j + 1] = key
    
    return arr, comparisons, shifts

# Read input
numbers = list(map(int, input().split()))

# Sort and count
sorted_numbers, comparisons, shifts = insertion_sort_with_counts(numbers)

# Output
print("Sorted:", " ".join(map(str, sorted_numbers)))
print("Comparisons:", comparisons)
print("Shifts:", shifts)