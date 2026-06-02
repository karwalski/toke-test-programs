def edit_distance_with_operations(source, target):
    m, n = len(source), len(target)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if source[i-1] == target[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # deletion
                    dp[i][j-1],    # insertion
                    dp[i-1][j-1]   # substitution
                )
    
    # Backtrack to find operations
    operations = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and source[i-1] == target[j-1]:
            # Characters match, no operation needed
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
            # Substitution
            operations.append(f"SUB({i-1},{source[i-1]},{target[j-1]})")
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            # Deletion
            operations.append(f"DEL({i-1},{source[i-1]})")
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j-1] + 1:
            # Insertion
            operations.append(f"INS({i},{target[j-1]})")
            j -= 1
    
    # Reverse operations to get correct order
    operations.reverse()
    
    return dp[m][n], operations

# Read input
source = input().strip()
target = input().strip()

# Compute edit distance and operations
distance, operations = edit_distance_with_operations(source, target)

# Output
print(f"Distance: {distance}")
print("Operations:")
for op in operations:
    print(op)