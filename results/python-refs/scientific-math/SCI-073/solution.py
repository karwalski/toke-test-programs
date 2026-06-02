def knapsack_01():
    # Read input
    capacity = int(input())
    n = int(input())
    
    items = []
    for i in range(n):
        line = input().split()
        weight = int(line[0])
        value = int(line[1])
        name = line[2]
        items.append((weight, value, name))
    
    # DP table: dp[i][w] = maximum value using first i items with capacity w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Fill DP table
    for i in range(1, n + 1):
        weight, value, name = items[i-1]
        for w in range(capacity + 1):
            # Don't take item i
            dp[i][w] = dp[i-1][w]
            # Take item i if possible
            if w >= weight:
                dp[i][w] = max(dp[i][w], dp[i-1][w-weight] + value)
    
    # Backtrack to find which items were selected
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(items[i-1][2])  # Add item name
            w -= items[i-1][0]  # Reduce capacity by item weight
    
    # Reverse to get correct order
    selected_items.reverse()
    
    # Calculate total weight
    total_weight = sum(items[i][0] for i in range(n) if items[i][2] in selected_items)
    
    # Output
    print(f"Max value: {dp[n][capacity]}")
    print(f"Items: {' '.join(selected_items)}")
    print(f"Total weight: {total_weight}")

knapsack_01()