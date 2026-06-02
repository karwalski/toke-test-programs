def solve_coin_change():
    # Read input
    coins = list(map(int, input().split()))
    target = int(input())
    
    # DP array to store minimum coins needed for each amount
    dp = [float('inf')] * (target + 1)
    dp[0] = 0
    
    # Array to track which coin was used to reach each amount
    parent = [-1] * (target + 1)
    
    # Fill DP table
    for amount in range(1, target + 1):
        for coin in coins:
            if coin <= amount and dp[amount - coin] + 1 < dp[amount]:
                dp[amount] = dp[amount - coin] + 1
                parent[amount] = coin
    
    # If target amount cannot be made
    if dp[target] == float('inf'):
        print("Minimum coins: -1")
        return
    
    # Backtrack to find coins used
    coins_used = []
    current = target
    while current > 0:
        coin = parent[current]
        coins_used.append(coin)
        current -= coin
    
    # Count frequency of each coin
    coin_count = {}
    for coin in coins_used:
        coin_count[coin] = coin_count.get(coin, 0) + 1
    
    # Sort by coin value
    sorted_coins = sorted(coin_count.items())
    
    # Format output
    print(f"Minimum coins: {dp[target]}")
    coins_str = " ".join([f"{count}x{coin}" for coin, count in sorted_coins])
    print(f"Coins used: {coins_str}")

solve_coin_change()