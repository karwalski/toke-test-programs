from itertools import combinations

def parse_card(card):
    """Parse a card string into rank and suit"""
    rank = card[:-1]
    suit = card[-1]
    return rank, suit

def card_value(rank):
    """Get the numeric value of a card for fifteens"""
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 1
    else:
        return int(rank)

def card_rank_value(rank):
    """Get the rank value for runs (A=1, 2=2, ..., J=11, Q=12, K=13)"""
    if rank == 'A':
        return 1
    elif rank == 'J':
        return 11
    elif rank == 'Q':
        return 12
    elif rank == 'K':
        return 13
    else:
        return int(rank)

def count_fifteens(cards):
    """Count all combinations that sum to 15"""
    values = [card_value(rank) for rank, suit in cards]
    count = 0
    
    # Check all possible combinations of cards
    for r in range(2, len(cards) + 1):
        for combo in combinations(values, r):
            if sum(combo) == 15:
                count += 1
    
    return count * 2  # Each fifteen is worth 2 points

def count_pairs(cards):
    """Count pairs (same rank)"""
    ranks = [rank for rank, suit in cards]
    rank_counts = {}
    
    for rank in ranks:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
    
    points = 0
    for count in rank_counts.values():
        if count >= 2:
            # n cards of same rank = n*(n-1)/2 pairs
            points += count * (count - 1) // 2 * 2
    
    return points

def count_runs(cards):
    """Count runs (consecutive ranks)"""
    ranks = [rank for rank, suit in cards]
    rank_values = [card_rank_value(rank) for rank in ranks]
    rank_counts = {}
    
    for rank in ranks:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
    
    # Get unique rank values and sort them
    unique_ranks = sorted(set(rank_values))
    
    # Find the longest consecutive sequence
    max_run_length = 0
    current_run_length = 1
    
    if len(unique_ranks) < 2:
        return 0
    
    for i in range(1, len(unique_ranks)):
        if unique_ranks[i] == unique_ranks[i-1] + 1:
            current_run_length += 1
        else:
            max_run_length = max(max_run_length, current_run_length)
            current_run_length = 1
    
    max_run_length = max(max_run_length, current_run_length)
    
    if max_run_length < 3:
        return 0
    
    # Calculate points: run length * product of counts of cards in run
    run_start = None
    for i in range(len(unique_ranks) - max_run_length + 1):
        consecutive = True
        for j in range(max_run_length - 1):
            if unique_ranks[i + j + 1] != unique_ranks[i + j] + 1:
                consecutive = False
                break
        if consecutive:
            run_start = i
            break
    
    if run_start is None:
        return 0
    
    # Calculate multiplier based on duplicate cards in the run
    multiplier = 1
    for i in range(run_start, run_start + max_run_length):
        rank_val = unique_ranks[i]
        # Find the rank name for this value
        for rank in rank_counts:
            if card_rank_value(rank) == rank_val:
                multiplier *= rank_counts[rank]
                break
    
    return max_run_length * multiplier

def count_flush(hand_cards, starter_card):
    """Count flush points"""
    hand_suits = [suit for rank, suit in hand_cards]
    starter_suit = starter_card[1]
    
    # Check if all hand cards are same suit
    if all(suit == hand_suits[0] for suit in hand_suits):
        if starter_suit == hand_suits[0]:
            return 5  # All 5 cards same suit
        else:
            return 4  # Only hand cards same suit
    
    return 0

def count_nobs(hand_cards, starter_card):
    """Count nobs (Jack in hand matching starter suit)"""
    starter_suit = starter_card[1]
    
    for rank, suit in hand_cards:
        if rank == 'J' and suit == starter_suit:
            return 1
    
    return 0

def main():
    # Read input
    cards_input = input().strip().split()
    
    # Parse cards
    hand_cards = [parse_card(card) for card in cards_input[:4]]
    starter_card = parse_card(cards_input[4])
    
    # All 5 cards for scoring
    all_cards = hand_cards + [starter_card]
    
    # Calculate scores
    fifteens = count_fifteens(all_cards)
    pairs = count_pairs(all_cards)
    runs = count_runs(all_cards)
    flush = count_flush(hand_cards, starter_card)
    nobs = count_nobs(hand_cards, starter_card)
    
    total = fifteens + pairs + runs + flush + nobs
    
    # Output
    print(f"Fifteens: {fifteens}")
    print(f"Pairs: {pairs}")
    print(f"Runs: {runs}")
    print(f"Flush: {flush}")
    print(f"Nobs: {nobs}")
    print(f"Total: {total}")

if __name__ == "__main__":
    main()