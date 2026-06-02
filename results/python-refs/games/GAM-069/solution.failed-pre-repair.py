def simulate_move(p1_pits, p2_pits, p1_store, p2_store, current_player, move_pit):
    # Make copies to avoid modifying original
    p1 = p1_pits[:]
    p2 = p2_pits[:]
    store1 = p1_store
    store2 = p2_store
    
    if current_player == 1:
        # Player 1 makes a move
        stones = p1[move_pit]
        p1[move_pit] = 0
        
        # Distribute stones counter-clockwise
        current_pos = move_pit
        while stones > 0:
            current_pos += 1
            
            # Player 1's side (pits 0-5)
            if current_pos <= 5:
                p1[current_pos] += 1
                stones -= 1
            # Player 1's store
            elif current_pos == 6:
                store1 += 1
                stones -= 1
            # Player 2's side (pits 5-0, going backwards)
            elif current_pos <= 12:
                p2_idx = 12 - current_pos
                p2[p2_idx] += 1
                stones -= 1
            # Reset to start of Player 1's side
            else:
                current_pos = -1  # Will become 0 after increment
                
    else:
        # Player 2 makes a move
        stones = p2[move_pit]
        p2[move_pit] = 0
        
        # Distribute stones counter-clockwise from Player 2's perspective
        current_pos = move_pit
        while stones > 0:
            current_pos += 1
            
            # Player 2's side (pits 0-5)
            if current_pos <= 5:
                p2[current_pos] += 1
                stones -= 1
            # Player 2's store
            elif current_pos == 6:
                store2 += 1
                stones -= 1
            # Player 1's side (pits 5-0, going backwards)
            elif current_pos <= 12:
                p1_idx = 12 - current_pos
                p1[p1_idx] += 1
                stones -= 1
            # Reset to start of Player 2's side
            else:
                current_pos = -1  # Will become 0 after increment
    
    return p1, p2, store1, store2

# Read input
p1_pits = list(map(int, input().split()))
p2_pits = list(map(int, input().split()))
stores = list(map(int, input().split()))
p1_store, p2_store = stores[0], stores[1]
current_player = int(input())

# Find valid moves and simulate them
for move in range(6):
    if current_player == 1:
        if p1_pits[move] > 0:  # Valid move if pit has stones
            new_p1, new_p2, new_store1, new_store2 = simulate_move(
                p1_pits, p2_pits, p1_store, p2_store, current_player, move
            )
            print(f"Move {move + 1}: {' '.join(map(str, new_p1))} | {' '.join(map(str, new_p2))} | {new_store1} {new_store2}")
    else:
        if p2_pits[move] > 0:  # Valid move if pit has stones
            new_p1, new_p2, new_store1, new_store2 = simulate_move(
                p1_pits, p2_pits, p1_store, p2_store, current_player, move
            )
            print(f"Move {move + 1}: {' '.join(map(str, new_p1))} | {' '.join(map(str, new_p2))} | {new_store1} {new_store2}")