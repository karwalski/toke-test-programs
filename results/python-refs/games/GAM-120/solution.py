import sys
from collections import deque

def solve_coin_change():
    target = int(input().strip())
    coins = list(map(int, input().strip().split()))
    
    # BFS to find minimum coins
    queue = deque([(0, [])])  # (current_amount, coins_used)
    visited = set([0])
    
    while queue:
        current_amount, coins_used = queue.popleft()
        
        if current_amount == target:
            if coins_used:
                coins_used.sort(reverse=True)
                result = ' '.join(map(str, coins_used))
                print(f"{result}: {len(coins_used)} coins")
            else:
                print("0: 0 coins")
            return
        
        for coin in coins:
            new_amount = current_amount + coin
            if new_amount <= target and new_amount not in visited:
                visited.add(new_amount)
                queue.append((new_amount, coins_used + [coin]))
    
    print("Impossible")

solve_coin_change()