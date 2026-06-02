def matrix_chain_multiplication():
    n = int(input())
    dims = list(map(int, input().split()))
    
    # dp[i][j] = minimum multiplications for matrices i to j
    dp = [[0] * n for _ in range(n)]
    # split[i][j] = optimal split point for matrices i to j
    split = [[0] * n for _ in range(n)]
    
    # Fill DP table
    for length in range(2, n + 1):  # chain length
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + dims[i] * dims[k+1] * dims[j+1]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k
    
    # Reconstruct parenthesization
    def build_expression(i, j):
        if i == j:
            return f"A{i}"
        else:
            k = split[i][j]
            left = build_expression(i, k)
            right = build_expression(k+1, j)
            return f"({left} x {right})"
    
    min_multiplications = dp[0][n-1]
    parenthesization = build_expression(0, n-1)
    
    print(f"Minimum multiplications: {min_multiplications}")
    print(f"Parenthesisation: {parenthesization}")

matrix_chain_multiplication()