def lomuto_partition(arr, low, high, pivots_chosen, comparisons):
    # Choose the last element as pivot
    pivot = arr[high]
    pivots_chosen.append(pivot)
    
    i = low - 1  # Index of smaller element
    
    for j in range(low, high):
        comparisons[0] += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quicksort(arr, low, high, pivots_chosen, comparisons):
    if low < high:
        pi = lomuto_partition(arr, low, high, pivots_chosen, comparisons)
        quicksort(arr, low, pi - 1, pivots_chosen, comparisons)
        quicksort(arr, pi + 1, high, pivots_chosen, comparisons)

# Read input
numbers = list(map(int, input().split()))

# Initialize tracking variables
pivots_chosen = []
comparisons = [0]  # Using list to make it mutable in recursive calls

# Sort the array
quicksort(numbers, 0, len(numbers) - 1, pivots_chosen, comparisons)

# Output results
print("Sorted:", " ".join(map(str, numbers)))
print("Pivots chosen:", " ".join(map(str, pivots_chosen)))
print("Comparisons:", comparisons[0])