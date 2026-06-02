import random
from itertools import combinations

def parse_card(card_str):
    if card_str == '.':
        return None
    rank = card_str[0]
    suit = card_str[1]
    return (rank, suit)

def card_to_value(rank):
    if rank == 'A':
        return 14
    elif rank == 'K':
        return 13
    elif rank == 'Q':
        return 12
    elif rank == 'J':
        return 11
    elif rank == 'T':
        return 10
    else:
        return int(rank)

def get_hand_rank(cards):
    # cards is a list of 7 cards (2 hole + 5 community)
    # Find the best 5-card hand
    best_rank = (0,)
    
    for combo in combinations(cards, 5):
        rank = evaluate_5_cards(combo)
        if rank > best_rank:
            best_rank = rank
    
    return best_rank

def evaluate_5_cards(cards):
    # Convert to (value, suit) and sort by value
    card_values = [(card_to_value(rank), suit) for rank, suit in cards]
    card_values.sort(key=lambda x: x[0], reverse=True)
    
    values = [v for v, s in card_values]
    suits = [s for v, s in card_values]
    
    # Count occurrences
    value_counts = {}
    for v in values:
        value_counts[v] = value_counts.get(v, 0) + 1
    
    counts = sorted(value_counts.values(), reverse=True)
    unique_values = sorted(value_counts.keys(), reverse=True)
    
    # Check for flush
    is_flush = len(set(suits)) == 1
    
    # Check for straight
    is_straight = False
    straight_high = 0
    
    # Normal straight check
    if len(set(values)) == 5 and max(values) - min(values) == 4:
        is_straight = True
        straight_high = max(values)
    
    # Ace-low straight (A,5,4,3,2)
    elif values == [14, 5, 4, 3, 2]:
        is_straight = True
        straight_high = 5
    
    # Hand rankings (higher tuple = better hand)
    if is_straight and is_flush:
        if straight_high == 14:
            return (9, 14)  # Royal flush
        else:
            return (8, straight_high)  # Straight flush
    
    elif counts == [4, 1]:  # Four of a kind
        four_kind = [v for v, c in value_counts.items() if c == 4][0]
        kicker = [v for v, c in value_counts.items() if c == 1][0]
        return (7, four_kind, kicker)
    
    elif counts == [3, 2]:  # Full house
        three_kind = [v for v, c in value_counts.items() if c == 3][0]
        pair = [v for v, c in value_counts.items() if c == 2][0]
        return (6, three_kind, pair)
    
    elif is_flush:  # Flush
        return (5,) + tuple(values)
    
    elif is_straight:  # Straight
        return (4, straight_high)
    
    elif counts == [3, 1, 1]:  # Three of a kind
        three_kind = [v for v, c in value_counts.items() if c == 3][0]
        kickers = sorted([v for v, c in value_counts.items() if c == 1], reverse=True)
        return (3, three_kind) + tuple(kickers)
    
    elif counts == [2, 2, 1]:  # Two pair
        pairs = sorted([v for v, c in value_counts.items() if c == 2], reverse=True)
        kicker = [v for v, c in value_counts.items() if c == 1][0]
        return (2, pairs[0], pairs[1], kicker)
    
    elif counts == [2, 1, 1, 1]:  # One pair
        pair = [v for v, c in value_counts.items() if c == 2][0]
        kickers = sorted([v for v, c in value_counts.items() if c == 1], reverse=True)
        return (1, pair) + tuple(kickers)
    
    else:  # High card
        return (0,) + tuple(values)

def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    suits = ['H', 'D', 'C', 'S']
    return [(rank, suit) for rank in ranks for suit in suits]

def main():
    # Read input
    hand1_line = input().strip()
    hand2_line = input().strip()
    community_line = input().strip()
    params_line = input().strip()
    
    hand1_cards = [parse_card(c) for c in hand1_line.split()]
    hand2_cards = [parse_card(c) for c in hand2_line.split()]
    community_cards = [parse_card(c) for c in community_line.split()]
    
    sample_count, seed = map(int, params_line.split())
    
    # Set random seed
    random.seed(seed)
    
    # Get known cards
    known_cards = []
    for card in hand1_cards + hand2_cards + community_cards:
        if card is not None:
            known_cards.append(card)
    
    # Create available deck
    full_deck = create_deck()
    available_cards = [card for card in full_deck if card not in known_cards]
    
    wins = 0
    ties = 0
    losses = 0
    
    for _ in range(sample_count):
        # Shuffle available cards
        random.shuffle(available_cards)
        
        # Deal unknown cards
        deck_index = 0
        
        # Complete community cards
        final_community = []
        for card in community_cards:
            if card is None:
                final_community.append(available_cards[deck_index])
                deck_index += 1
            else:
                final_community.append(card)
        
        # Evaluate both hands
        hand1_all = hand1_cards + final_community
        hand2_all = hand2_cards + final_community
        
        hand1_rank = get_hand_rank(hand1_all)
        hand2_rank = get_hand_rank(hand2_all)
        
        if hand1_rank > hand2_rank:
            wins += 1
        elif hand1_rank < hand2_rank:
            losses += 1
        else:
            ties += 1
    
    # Calculate percentages
    win_pct = (wins / sample_count) * 100
    tie_pct = (ties / sample_count) * 100
    lose_pct = (losses / sample_count) * 100
    
    # Output
    print(f"Win: {win_pct:.2f}% Tie: {tie_pct:.2f}% Lose: {lose_pct:.2f}%")

if __name__ == "__main__":
    main()