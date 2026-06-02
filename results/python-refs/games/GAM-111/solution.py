import sys
from itertools import combinations

def parse_card(card_str):
    # Parse a card string like "1R1S" into (number, color, count, shading)
    return (card_str[0], card_str[1], card_str[2], card_str[3])

def is_valid_set(card1, card2, card3):
    # Check if three cards form a valid set
    # For each attribute, all three cards must have either all same or all different values
    for i in range(4):
        values = [card1[i], card2[i], card3[i]]
        # Check if all same or all different
        if len(set(values)) == 2:  # This means we have 2 same and 1 different, which is invalid
            return False
    return True

# Read input
cards = []
for line in sys.stdin:
    line = line.strip()
    if line:
        cards.append(parse_card(line))

# Find all valid sets
valid_sets = []
for combo in combinations(range(len(cards)), 3):
    i, j, k = combo
    if is_valid_set(cards[i], cards[j], cards[k]):
        valid_sets.append((i, j, k))

# Output results
for valid_set in valid_sets:
    print(f"{valid_set[0]} {valid_set[1]} {valid_set[2]}")