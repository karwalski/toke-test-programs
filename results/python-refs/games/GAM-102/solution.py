# Read input
player1_cards = input().split()
player2_cards = input().split()

# Initialize variables
pile = []
turn = 0
snaps = []

# Simulate the game
max_turns = min(len(player1_cards), len(player2_cards))

for i in range(max_turns):
    turn += 1
    
    # Player 1 plays first, then Player 2
    p1_card = player1_cards[i]
    pile.append(p1_card)
    
    # Check for snap after Player 1's card
    if len(pile) >= 2 and pile[-1] == pile[-2]:
        snaps.append(turn)
        print(f"Snap! at turn {turn}")
    
    # Player 2 plays
    p2_card = player2_cards[i]
    pile.append(p2_card)
    
    # Check for snap after Player 2's card
    if len(pile) >= 2 and pile[-1] == pile[-2]:
        snaps.append(turn)
        print(f"Snap! at turn {turn}")

# Calculate final score
snap_count = len(snaps)
if snap_count > 0:
    print(f"Player 1 wins {snap_count * 2}-0")
else:
    print("Player 1 wins 0-0")