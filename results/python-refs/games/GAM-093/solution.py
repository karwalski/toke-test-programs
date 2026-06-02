def card_value(card):
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)

def calculate_total(cards):
    total = 0
    aces = 0
    
    for card in cards:
        if card == 'A':
            aces += 1
            total += 11
        elif card in ['J', 'Q', 'K']:
            total += 10
        else:
            total += int(card)
    
    # Adjust for aces
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    
    return total

# Read input
initial_hand = input().split()
deck = input().split()

# Calculate initial total
total = calculate_total(initial_hand)

# Check initial state
if total >= 17:
    print(f"Stand: {total}")
else:
    print(f"Stand: {total}")
    
    # Dealer hits
    deck_index = 0
    while total <= 16 and deck_index < len(deck):
        card = deck[deck_index]
        deck_index += 1
        
        # Add card value
        if card == 'A':
            total += 11
            # Adjust for ace if needed
            if total > 21:
                total -= 10
        elif card in ['J', 'Q', 'K']:
            total += 10
        else:
            total += int(card)
        
        # Check result
        if total > 21:
            print(f"Hit: {card} -> Bust: {total}")
            break
        elif total >= 17:
            print(f"Hit: {card} -> Stand: {total}")
            break
        else:
            print(f"Hit: {card} -> {total}")