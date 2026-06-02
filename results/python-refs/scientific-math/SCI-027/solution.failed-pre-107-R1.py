def merge_sort(arr, depth=0):
    global max_depth, comparisons
    max_depth = max(max_depth, depth)
    
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], depth + 1)
    right = merge_sort(arr[mid:], depth + 1)
    
    return merge(left, right)

def merge(left, right):
    global comparisons
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

# Read input
numbers = list(map(int, input().split()))

# Initialize global variables
max_depth = 0
comparisons = 0

# Sort the list
sorted_numbers = merge_sort(numbers)

# Output results
print("Sorted:", " ".join(map(str, sorted_numbers)))
print("Merge depth:", max_depth)
print("Comparisons:", comparisons)