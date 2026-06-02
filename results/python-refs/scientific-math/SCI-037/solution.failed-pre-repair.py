def lcs_length_and_subsequence(A, B):
    m, n = len(A), len(B)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if A[i-1] == B[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # Backtrack to find one LCS
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if A[i-1] == B[j-1]:
            lcs.append(A[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    lcs.reverse()
    return dp[m][n], ''.join(lcs)

# Read input
A = input().strip()
B = input().strip()

# Find LCS
length, subsequence = lcs_length_and_subsequence(A, B)

# Output result
print(f"LCS length: {length}")
print(f"LCS: {subsequence}")