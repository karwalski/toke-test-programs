def quicksort_with_logging(arr, start=0, end=None):
    if end is None:
        end = len(arr) - 1
    
    if start < end:
        # Choose pivot (last element)
        pivot_index = partition(arr, start, end)

def partition(arr, start, end):
    pivot = arr[end]
    
    # Partition the array
    left_part = []
    right_part = []
    
    for i in range(start, end):
        if arr[i] <= pivot:
            left_part.append(arr[i])
        else:
            right_part.append(arr[i])
    
    # Print the partition result
    left_str = "[" + ",".join(map(str, left_part)) + "]" if left_part else "[]"
    right_str = "[" + ",".join(map(str, right_part)) + "]" if right_part else "[]"
    print(f"Pivot: {pivot} -> {left_str} {pivot} {right_str}")
    
    # Reconstruct the array segment
    new_arr = left_part + [pivot] + right_part
    for i, val in enumerate(new_arr):
        arr[start + i] = val
    
    return start + len(left_part)

def quicksort_recursive(arr, start, end):
    if start < end:
        pivot_index = partition(arr, start, end)
        quicksort_recursive(arr, start, pivot_index - 1)
        quicksort_recursive(arr, pivot_index + 1, end)

# Read input
input_line = input().strip()
numbers = list(map(int, input_line.split()))

# Perform quicksort with logging
quicksort_recursive(numbers, 0, len(numbers) - 1)

# Print final sorted result
print("Sorted:", " ".join(map(str, numbers)))