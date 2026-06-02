pot, bet = map(int, input().split())

pot_odds = bet / (pot + bet) * 100
min_equity = pot_odds

print(f"Pot odds: {pot_odds:.2f}%")
print(f"Minimum equity: {min_equity:.2f}%")