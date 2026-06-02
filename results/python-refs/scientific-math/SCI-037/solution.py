import sys

def lcs_smallest(A, B):
    m, n = len(A), len(B)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if A[i-1] == B[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    L = dp[m][n]
    
    # For each (i,j), precompute next position of each char in A[i:] and B[j:]
    # nextA[i][c] = smallest k >= i such that A[k] == c, or m if none
    nextA = [[m]*26 for _ in range(m+1)]
    for i in range(m-1, -1, -1):
        for c in range(26):
            nextA[i][c] = nextA[i+1][c]
        nextA[i][ord(A[i])-ord('A')] = i
    
    nextB = [[n]*26 for _ in range(n+1)]
    for i in range(n-1, -1, -1):
        for c in range(26):
            nextB[i][c] = nextB[i+1][c]
        nextB[i][ord(B[i])-ord('A')] = i
    
    # Greedy: at each step pick smallest char c such that there are positions
    # i' >= i, j' >= j with A[i']=B[j']=c and LCS of A[i'+1:], B[j'+1:] >= remaining-1
    result = []
    i, j = 0, 0
    remaining = L
    while remaining > 0:
        for c in range(26):
            ia = nextA[i][c]
            jb = nextB[j][c]
            if ia < m and jb < n:
                if dp[m - (ia+1) if False else ia+1][jb+1] if False else dp[ia+1][jb+1] >= remaining - 1:
                    # Wait, dp[ia+1][jb+1] is LCS of A[:ia+1], B[:jb+1], not suffix
                    pass
        # Need suffix dp
        break
    
    # Redo with suffix dp
    sdp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m-1, -1, -1):
        for j in range(n-1, -1, -1):
            if A[i] == B[j]:
                sdp[i][j] = sdp[i+1][j+1] + 1
            else:
                sdp[i][j] = max(sdp[i+1][j], sdp[i][j+1])
    
    result = []
    i, j = 0, 0
    remaining = L
    while remaining > 0:
        for c in range(26):
            ia = nextA[i][c]
            jb = nextB[j][c]
            if ia < m and jb < n:
                if sdp[ia+1][jb+1] >= remaining - 1:
                    result.append(chr(ord('A')+c))
                    i = ia + 1
                    j = jb + 1
                    remaining -= 1
                    break
    return L, ''.join(result)

data = sys.stdin.read().split('\n')
A = data[0].strip()
B = data[1].strip()
length, sub = lcs_smallest(A, B)
print(f"LCS length: {length}")
print(f"LCS: {sub}")