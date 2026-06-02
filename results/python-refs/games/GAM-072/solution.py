import sys

def get_card_value(card):
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)

def get_hand_value(cards):
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

def is_soft(cards):
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
    
    # Check if we have an ace counting as 11
    if aces > 0 and total <= 21:
        return True
    return False

def is_pair(cards):
    if len(cards) != 2:
        return False
    
    card1, card2 = cards
    
    # Handle face cards
    if card1 in ['J', 'Q', 'K'] and card2 in ['J', 'Q', 'K']:
        return True
    
    return card1 == card2

def basic_strategy(player_cards, dealer_card):
    dealer_value = get_card_value(dealer_card)
    
    # Check for pairs first
    if is_pair(player_cards):
        pair_card = player_cards[0]
        if pair_card == 'A':
            return "Split"
        elif pair_card == '8':
            return "Split"
        elif pair_card in ['2', '3']:
            if dealer_value in [2, 3, 4, 5, 6, 7]:
                return "Split"
            else:
                return "Hit"
        elif pair_card == '4':
            if dealer_value in [5, 6]:
                return "Split"
            else:
                return "Hit"
        elif pair_card == '5':
            if dealer_value in [2, 3, 4, 5, 6, 7, 8, 9]:
                return "Double"
            else:
                return "Hit"
        elif pair_card == '6':
            if dealer_value in [2, 3, 4, 5, 6]:
                return "Split"
            else:
                return "Hit"
        elif pair_card == '7':
            if dealer_value in [2, 3, 4, 5, 6, 7]:
                return "Split"
            else:
                return "Hit"
        elif pair_card == '9':
            if dealer_value in [2, 3, 4, 5, 6, 8, 9]:
                return "Split"
            else:
                return "Stand"
        elif pair_card in ['10', 'J', 'Q', 'K']:
            return "Stand"
    
    hand_value = get_hand_value(player_cards)
    
    # Soft hands (with ace counting as 11)
    if is_soft(player_cards) and len(player_cards) == 2:
        soft_value = hand_value - 11  # The value of the other card
        
        if soft_value in [2, 3]:  # A,2 or A,3
            if dealer_value in [5, 6]:
                return "Double"
            else:
                return "Hit"
        elif soft_value in [4, 5]:  # A,4 or A,5
            if dealer_value in [4, 5, 6]:
                return "Double"
            else:
                return "Hit"
        elif soft_value in [6, 7]:  # A,6 or A,7
            if soft_value == 6:
                if dealer_value in [3, 4, 5, 6]:
                    return "Double"
                else:
                    return "Hit"
            else:  # A,7
                if dealer_value in [3, 4, 5, 6]:
                    return "Double"
                elif dealer_value in [2, 7, 8]:
                    return "Stand"
                else:
                    return "Hit"
        elif soft_value >= 8:  # A,8 or A,9
            return "Stand"
    
    # Hard hands
    if hand_value <= 8:
        return "Hit"
    elif hand_value == 9:
        if dealer_value in [3, 4, 5, 6]:
            return "Double"
        else:
            return "Hit"
    elif hand_value == 10:
        if dealer_value in [2, 3, 4, 5, 6, 7, 8, 9]:
            return "Double"
        else:
            return "Hit"
    elif hand_value == 11:
        if dealer_value in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
            return "Double"
        else:
            return "Hit"
    elif hand_value == 12:
        if dealer_value in [4, 5, 6]:
            return "Stand"
        else:
            return "Hit"
    elif hand_value in [13, 14, 15, 16]:
        if dealer_value in [2, 3, 4, 5, 6]:
            return "Stand"
        else:
            return "Hit"
    else:  # 17 or higher
        return "Stand"

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

player_cards = lines[0].split()
dealer_card = lines[1]

result = basic_strategy(player_cards, dealer_card)
print(result)