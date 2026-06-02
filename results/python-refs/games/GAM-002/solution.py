def classify_poker_hand(cards):
    # Parse cards into ranks and suits
    ranks = []
    suits = []
    
    for card in cards:
        if card.startswith('10'):
            rank = '10'
            suit = card[2]
        else:
            rank = card[:-1]
            suit = card[-1]
        ranks.append(rank)
        suits.append(suit)
    
    # Convert ranks to numbers for easier comparison
    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
                   '9': 9, '10': 10, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    
    numeric_ranks = [rank_values[rank] for rank in ranks]
    numeric_ranks.sort()
    
    # Count rank frequencies
    rank_counts = {}
    for rank in numeric_ranks:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
    
    # Check for flush
    is_flush = len(set(suits)) == 1
    
    # Check for straight
    is_straight = False
    if len(set(numeric_ranks)) == 5:
        if numeric_ranks[4] - numeric_ranks[0] == 4:
            is_straight = True
        # Special case: A-2-3-4-5 straight (wheel)
        elif numeric_ranks == [2, 3, 4, 5, 14]:
            is_straight = True
    
    # Check for royal flush (A-K-Q-J-10 all same suit)
    if is_flush and is_straight and numeric_ranks == [10, 11, 12, 13, 14]:
        return "Royal Flush"
    
    # Check for straight flush
    if is_flush and is_straight:
        return "Straight Flush"
    
    # Check for four of a kind
    if 4 in rank_counts.values():
        return "Four of a Kind"
    
    # Check for full house
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        return "Full House"
    
    # Check for flush
    if is_flush:
        return "Flush"
    
    # Check for straight
    if is_straight:
        return "Straight"
    
    # Check for three of a kind
    if 3 in rank_counts.values():
        return "Three of a Kind"
    
    # Check for pairs
    pair_count = sum(1 for count in rank_counts.values() if count == 2)
    
    if pair_count == 2:
        return "Two Pair"
    elif pair_count == 1:
        return "Pair"
    else:
        return "High Card"

# Read input and process
line = input().strip()
cards = line.split()
result = classify_poker_hand(cards)
print(result)