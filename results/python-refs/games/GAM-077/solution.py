def knapsack_01(capacity, items):
    n = len(items)
    # dp[i][w] = maximum value using first i items with weight limit w
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # Fill the dp table
    for i in range(1, n + 1):
        name, weight, value = items[i-1]
        for w in range(capacity + 1):
            # Don't take item i
            dp[i][w] = dp[i-1][w]
            # Take item i if possible
            if weight <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w-weight] + value)
    
    # Backtrack to find which items were selected
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(items[i-1][0])  # Add item name
            w -= items[i-1][1]  # Subtract item weight
    
    selected.reverse()  # Reverse to get original order
    return selected, dp[n][capacity]

# Read input
capacity = int(input())
items = []

try:
    while True:
        line = input().strip()
        if line:
            parts = line.split()
            name = parts[0]
            weight = int(parts[1])
            value = int(parts[2])
            items.append((name, weight, value))
except EOFError:
    pass

# Solve knapsack
selected_items, total_value = knapsack_01(capacity, items)

# Output
print(' '.join(selected_items))
print(f'Total value: {total_value}')