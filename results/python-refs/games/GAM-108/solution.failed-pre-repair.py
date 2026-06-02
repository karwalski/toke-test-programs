import sys

def calculate_elo_change(rating_a, rating_b, result, k=32):
    """Calculate the change in Elo rating for player A"""
    expected_a = 1 / (1 + 10**((rating_b - rating_a) / 400))
    change_a = k * (result - expected_a)
    return change_a

def main():
    # Read initial ratings
    ratings = {}
    
    # Read player ratings until blank line
    for line in sys.stdin:
        line = line.strip()
        if not line:
            break
        parts = line.split()
        player = parts[0]
        rating = int(parts[1])
        ratings[player] = rating
    
    # Read game results
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split()
        player1 = parts[0]
        player2 = parts[1]
        result = float(parts[2])
        
        # Calculate rating changes
        change1 = calculate_elo_change(ratings[player1], ratings[player2], result)
        change2 = calculate_elo_change(ratings[player2], ratings[player1], 1 - result)
        
        # Update ratings
        ratings[player1] += change1
        ratings[player2] += change2
    
    # Sort players by rating (descending) and output
    sorted_players = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    
    for player, rating in sorted_players:
        print(f"{player}: {int(round(rating))}")

if __name__ == "__main__":
    main()