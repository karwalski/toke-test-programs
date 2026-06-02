def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    merged = merge(left, right)
    
    # Only print merge operations for lists of size > 1
    if len(left) > 0 and len(right) > 0:
        left_str = "[" + ",".join(map(str, left)) + "]"
        right_str = "[" + ",".join(map(str, right)) + "]"
        merged_str = "[" + ",".join(map(str, merged)) + "]"
        print(f"Merge {left_str} + {right_str} -> {merged_str}")
    
    return merged

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    while i < len(left):
        result.append(left[i])
        i += 1
    
    while j < len(right):
        result.append(right[j])
        j += 1
    
    return result

# Read input
input_line = input().strip()
numbers = list(map(int, input_line.split()))

# Sort and get result
sorted_numbers = merge_sort(numbers)

# Print final result
print("Sorted:", " ".join(map(str, sorted_numbers)))