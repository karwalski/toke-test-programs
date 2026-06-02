def newton_divided_differences():
    n = int(input())
    
    # Read data points
    x = []
    y = []
    for _ in range(n):
        xi, yi = map(float, input().split())
        x.append(xi)
        y.append(yi)
    
    # Create divided difference table
    table = [[0 for _ in range(n)] for _ in range(n)]
    
    # Fill first column with y values
    for i in range(n):
        table[i][0] = y[i]
    
    # Fill the rest of the table
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = (table[i + 1][j - 1] - table[i][j - 1]) / (x[i + j] - x[i])
    
    # Print divided difference table
    for i in range(n):
        for j in range(n - i):
            if j == 0:
                print(f"{table[i][j]:.6f}", end="")
            else:
                print(f" {table[i][j]:.6f}", end="")
        print()
    
    # Read query values and interpolate
    try:
        while True:
            query_x = float(input())
            
            # Calculate interpolated value using Newton's formula
            result = table[0][0]
            product = 1.0
            
            for j in range(1, n):
                product *= (query_x - x[j - 1])
                result += table[0][j] * product
            
            print(f"p({query_x:.0f}) = {result:.6f}")
    except EOFError:
        pass

newton_divided_differences()