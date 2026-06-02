import random

def create_deck():
    suits = ['H', 'D', 'C', 'S']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(rank + suit)
    return deck

def main():
    line = input().strip()
    seed, num_hands, cards_per_hand = map(int, line.split())
    
    # Set the random seed
    random.seed(seed)
    
    # Create and shuffle the deck
    deck = create_deck()
    random.shuffle(deck)
    
    # Deal the hands
    card_index = 0
    for hand_num in range(1, num_hands + 1):
        hand = []
        for _ in range(cards_per_hand):
            hand.append(deck[card_index])
            card_index += 1
        print(f"Hand {hand_num}: {' '.join(hand)}")

if __name__ == "__main__":
    main()