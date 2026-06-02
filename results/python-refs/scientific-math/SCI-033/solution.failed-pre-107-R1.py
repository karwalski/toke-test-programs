def knuth_gaps(n):
    """Generate Knuth's gap sequence: 1, 4, 13, 40, ..."""
    gaps = []
    gap = 1
    while gap < n:
        gaps.append(gap)
        gap = 3 * gap + 1
    return gaps[::-1]  # Return in descending order

def shell_sort(arr):
    n = len(arr)
    gaps = knuth_gaps(n)
    gaps_used = []
    comparisons = 0
    
    for gap in gaps:
        if gap < n:  # Only use gaps that are meaningful for this array size
            gaps_used.append(gap)
            
            # Perform insertion sort with the current gap
            for i in range(gap, n):
                temp = arr[i]
                j = i
                
                while j >= gap:
                    comparisons += 1
                    if arr[j - gap] > temp:
                        arr[j] = arr[j - gap]
                        j -= gap
                    else:
                        break
                
                arr[j] = temp
    
    return gaps_used, comparisons

# Read input
numbers = list(map(int, input().split()))

# Sort using Shell sort
gaps_used, comparisons = shell_sort(numbers)

# Output results
print("Sorted:", " ".join(map(str, numbers)))
print("Gaps used:", " ".join(map(str, gaps_used)))
print("Comparisons:", comparisons)