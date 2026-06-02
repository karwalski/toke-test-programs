def find_lis(arr):
    n = len(arr)
    if n == 0:
        return 0, []
    
    # dp[i] stores the length of LIS ending at index i
    dp = [1] * n
    # parent[i] stores the previous index in the LIS ending at i
    parent = [-1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
    
    # Find the index with maximum LIS length
    max_length = max(dp)
    max_index = dp.index(max_length)
    
    # Reconstruct the LIS
    lis = []
    current = max_index
    while current != -1:
        lis.append(arr[current])
        current = parent[current]
    
    lis.reverse()
    return max_length, lis

# Read input
line = input().strip()
arr = list(map(int, line.split()))

# Find LIS
length, lis = find_lis(arr)

# Output
print(f"LIS length: {length}")
print(f"LIS: {' '.join(map(str, lis))}")