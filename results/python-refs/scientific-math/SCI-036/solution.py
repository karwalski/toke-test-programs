def levenshtein_with_alignment(s, t):
    m, n = len(s), len(t)
    
    # DP table for distances
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1]  # match
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],      # deletion
                    dp[i][j-1],      # insertion
                    dp[i-1][j-1]     # substitution
                )
    
    # Backtrack to find alignment
    i, j = m, n
    align_s, align_t = [], []
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + (0 if s[i-1] == t[j-1] else 1):
            # Match or substitution
            align_s.append(s[i-1])
            align_t.append(t[j-1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            # Deletion from s
            align_s.append(s[i-1])
            align_t.append('-')
            i -= 1
        else:
            # Insertion to s
            align_s.append('-')
            align_t.append(t[j-1])
            j -= 1
    
    align_s.reverse()
    align_t.reverse()
    
    return dp[m][n], ''.join(align_s), ''.join(align_t)

# Read input
s = input().strip()
t = input().strip()

# Compute distance and alignment
distance, aligned_s, aligned_t = levenshtein_with_alignment(s, t)

# Output
print(f"Distance: {distance}")
print("Alignment:")
print(aligned_s)
print(aligned_t)