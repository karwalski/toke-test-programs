prices = list(map(int, input().split()))
cash = int(input())
shares = 0

for i in range(len(prices)):
    command = input().strip()
    
    if command.startswith("buy"):
        num_shares = int(command.split()[1])
        cost = num_shares * prices[i]
        if cash >= cost:
            cash -= cost
            shares += num_shares
    elif command.startswith("sell"):
        num_shares = int(command.split()[1])
        if shares >= num_shares:
            cash += num_shares * prices[i]
            shares -= num_shares
    # hold command does nothing
    
    portfolio_value = cash + shares * prices[i]
    print(f"Day {i+1}: ${portfolio_value:.2f}")