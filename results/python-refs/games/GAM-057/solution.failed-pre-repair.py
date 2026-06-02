import sys

def play_game(move1, move2):
    """
    Returns result from player1's perspective:
    1 = win, 0 = draw, -1 = loss
    """
    if move1 == move2:
        return 0  # draw
    elif (move1 == 'R' and move2 == 'S') or \
         (move1 == 'P' and move2 == 'R') or \
         (move1 == 'S' and move2 == 'P'):
        return 1  # win
    else:
        return -1  # loss

def main():
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            lines.append(line)
    
    # Parse input
    players = []
    strategies = []
    
    # Last line is number of rounds
    num_rounds = int(lines[-1])
    
    # All other lines are player data
    for i in range(len(lines) - 1):
        parts = lines[i].split()
        name = parts[0]
        strategy = parts[1]
        players.append(name)
        strategies.append(strategy)
    
    n_players = len(players)
    
    # Initialize stats: [wins, draws, losses]
    stats = [[0, 0, 0] for _ in range(n_players)]
    
    # Play round-robin tournament for each round
    for round_num in range(num_rounds):
        for i in range(n_players):
            for j in range(i + 1, n_players):
                # Get moves for this round
                move1 = strategies[i][round_num % len(strategies[i])]
                move2 = strategies[j][round_num % len(strategies[j])]
                
                result = play_game(move1, move2)
                
                if result == 1:  # player i wins
                    stats[i][0] += 1  # win for i
                    stats[j][2] += 1  # loss for j
                elif result == 0:  # draw
                    stats[i][1] += 1  # draw for i
                    stats[j][1] += 1  # draw for j
                else:  # player i loses
                    stats[i][2] += 1  # loss for i
                    stats[j][0] += 1  # win for j
    
    # Create list of (player_index, wins, draws, losses) for sorting
    results = []
    for i in range(n_players):
        wins, draws, losses = stats[i]
        results.append((i, wins, draws, losses))
    
    # Sort by wins (descending), then by losses (ascending), then by name
    results.sort(key=lambda x: (-x[1], x[3], players[x[0]]))
    
    # Output results
    for rank, (player_idx, wins, draws, losses) in enumerate(results, 1):
        player_name = players[player_idx]
        print(f"{rank}. {player_name}: {wins}W {draws}D {losses}L")

if __name__ == "__main__":
    main()