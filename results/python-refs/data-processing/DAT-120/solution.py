def needleman_wunsch(seq1, seq2, match, mismatch, gap):
    m, n = len(seq1), len(seq2)
    
    # Initialize scoring matrix
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize first row and column
    for i in range(m + 1):
        dp[i][0] = i * gap
    for j in range(n + 1):
        dp[0][j] = j * gap
    
    # Fill the scoring matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i-1] == seq2[j-1]:
                diagonal = dp[i-1][j-1] + match
            else:
                diagonal = dp[i-1][j-1] + mismatch
            
            up = dp[i-1][j] + gap
            left = dp[i][j-1] + gap
            
            dp[i][j] = max(diagonal, up, left)
    
    # Traceback to get alignment
    align1, align2 = "", ""
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            if seq1[i-1] == seq2[j-1]:
                score_diag = dp[i-1][j-1] + match
            else:
                score_diag = dp[i-1][j-1] + mismatch
            
            if dp[i][j] == score_diag:
                align1 = seq1[i-1] + align1
                align2 = seq2[j-1] + align2
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i-1][j] + gap:
                align1 = seq1[i-1] + align1
                align2 = "-" + align2
                i -= 1
            else:
                align1 = "-" + align1
                align2 = seq2[j-1] + align2
                j -= 1
        elif i > 0:
            align1 = seq1[i-1] + align1
            align2 = "-" + align2
            i -= 1
        else:
            align1 = "-" + align1
            align2 = seq2[j-1] + align2
            j -= 1
    
    return dp[m][n], align1, align2

# Read input
line1 = input().split()
match_score = int(line1[0])
mismatch_penalty = int(line1[1])
gap_penalty = int(line1[2])

seq1 = input().strip()
seq2 = input().strip()

# Perform alignment
score, aligned1, aligned2 = needleman_wunsch(seq1, seq2, match_score, mismatch_penalty, gap_penalty)

# Output results
print(f"Score: {score}")
print(aligned1)
print(aligned2)