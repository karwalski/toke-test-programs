def heapify(arr, n, i, comparisons):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n:
        comparisons[0] += 1
        if arr[left] > arr[largest]:
            largest = left
    
    if right < n:
        comparisons[0] += 1
        if arr[right] > arr[largest]:
            largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, comparisons)

def build_max_heap(arr, comparisons):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, comparisons)

def heapsort(arr):
    comparisons = [0]
    n = len(arr)
    
    # Build max heap
    build_max_heap(arr, comparisons)
    heap_after_build = arr.copy()
    
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0, comparisons)
    
    return heap_after_build, arr, comparisons[0]

# Read input
numbers = list(map(int, input().split()))

# Sort using heapsort
heap_after_build, sorted_arr, comparison_count = heapsort(numbers)

# Output results
print("Heap after build:", " ".join(map(str, heap_after_build)))
print("Sorted:", " ".join(map(str, sorted_arr)))
print("Comparisons:", comparison_count)