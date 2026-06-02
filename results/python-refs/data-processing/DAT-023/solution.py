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
    for i in range(n // 2 - 1, -1, -1):
        heapify_down(arr, i, n)

def heap_sort(arr):
    n = len(arr)
    heap = arr[:]
    
    build_max_heap(heap)
    print("Heap:", " ".join(map(str, heap)))
    
    sorted_result = []
    
    for i in range(n):
        max_val = heap[0]
        sorted_result.append(max_val)
        
        heap[0] = heap[n - 1 - i]
        heap = heap[:n - 1 - i]
        
        if heap:
            heapify_down(heap, 0, len(heap))
            print(f"Extract {max_val}:", " ".join(map(str, heap)))
    
    sorted_result.reverse()
    return sorted_result

nums = list(map(int, input().split()))
sorted_nums = heap_sort(nums)
print("Sorted:", " ".join(map(str, sorted_nums)))