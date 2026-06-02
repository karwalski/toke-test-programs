def evaluate_blackjack_hand(cards):
    total = 0
    aces = 0
    
    for card in cards:
        if card in ['J', 'Q', 'K']:
            total += 10
        elif card == 'A':
            aces += 1
            total += 11
        else:
            total += int(card)
    
    # Convert aces from 11 to 1 if needed to avoid busting
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    
    return total

# Read input
cards = input().split()

# Calculate total
total = evaluate_blackjack_hand(cards)

# Output result
if total > 21:
    print(f"{total} Bust")
else:
    print(f"{total} Safe")