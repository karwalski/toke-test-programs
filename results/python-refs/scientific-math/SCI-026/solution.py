def selection_sort(arr):
    comparisons = 0
    swaps = 0
    n = len(arr)
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        swaps += 1
    
    return arr, comparisons, swaps

numbers = list(map(int, input().split()))
sorted_numbers, comparisons, swaps = selection_sort(numbers)
print("Sorted:", " ".join(map(str, sorted_numbers)))
print("Comparisons:", comparisons)
print("Swaps:", swaps)