import random

def main():
    seed = int(input().strip())
    random.seed(seed)
    
    # Create and shuffle deck
    deck = list(range(2, 15)) * 4  # 2-14 (Jack=11, Queen=12, King=13, Ace=14)
    random.shuffle(deck)
    
    # Deal cards to players
    player1_cards = deck[:26]
    player2_cards = deck[26:]
    
    rounds = 0
    
    while player1_cards and player2_cards:
        rounds += 1
        
        # Each player plays their top card
        card1 = player1_cards.pop(0)
        card2 = player2_cards.pop(0)
        
        if card1 > card2:
            # Player 1 wins the round
            player1_cards.extend([card1, card2])
        elif card2 > card1:
            # Player 2 wins the round
            player2_cards.extend([card2, card1])
        else:
            # War! Each player puts down 3 cards face down and 1 face up
            war_cards = [card1, card2]
            
            # Each player needs at least 4 cards for war (3 down + 1 up)
            if len(player1_cards) < 4 or len(player2_cards) < 4:
                # Not enough cards for war, whoever has more cards wins
                if len(player1_cards) > len(player2_cards):
                    player1_cards.extend(war_cards)
                    player2_cards.clear()
                else:
                    player2_cards.extend(war_cards)
                    player1_cards.clear()
                break
            
            # Each player puts 3 cards face down
            for _ in range(3):
                war_cards.append(player1_cards.pop(0))
                war_cards.append(player2_cards.pop(0))
            
            # Each player puts 1 card face up for comparison
            war_card1 = player1_cards.pop(0)
            war_card2 = player2_cards.pop(0)
            war_cards.extend([war_card1, war_card2])
            
            if war_card1 > war_card2:
                player1_cards.extend(war_cards)
            elif war_card2 > war_card1:
                player2_cards.extend(war_cards)
            else:
                # Another tie - for simplicity, player 1 wins
                player1_cards.extend(war_cards)
    
    if player1_cards:
        print(f"Player 1 wins after {rounds} rounds")
    else:
        print(f"Player 2 wins after {rounds} rounds")

if __name__ == "__main__":
    main()