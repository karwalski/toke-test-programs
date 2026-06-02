def heapify_down(heap, i, size):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < size and heap[left] > heap[largest]:
        largest = left
    
    if right < size and heap[right] > heap[largest]:
        largest = right
    
    if largest != i:
        heap[i], heap[largest] = heap[largest], heap[i]
        heapify_down(heap, largest, size)

def build_max_heap(arr):
    n = len(arr)
    # Start from the last non-leaf node and heapify down
    for i in range(n // 2 - 1, -1, -1):
        heapify_down(arr, i, n)

def heap_sort(arr):
    n = len(arr)
    heap = arr[:]
    
    # Build max heap
    build_max_heap(heap)
    print("Heap:", " ".join(map(str, heap)))
    
    sorted_result = []
    
    # Extract elements one by one
    for i in range(n):
        # Extract max (root)
        max_val = heap[0]
        sorted_result.append(max_val)
        
        # Move last element to root and reduce heap size
        heap[0] = heap[n - 1 - i]
        heap = heap[:n - 1 - i]
        
        # Heapify the reduced heap
        if heap:
            heapify_down(heap, 0, len(heap))
        
        # Print extraction step
        if heap:
            print(f"Extract {max_val}:", " ".join(map(str, heap)))
        else:
            print(f"Extract {max_val}:")
    
    return sorted_result

# Read input
nums = list(map(int, input().split()))

# Perform heap sort
sorted_nums = heap_sort(nums)

# Print sorted result
print("Sorted:", " ".join(map(str, sorted_nums)))