import sys
from collections import defaultdict

def main():
    scores = defaultdict(int)
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split()
        command = parts[0]
        
        if command == "score":
            player = parts[1]
            score = int(parts[2])
            scores[player] = score
            
        elif command == "rank":
            player = parts[1]
            player_score = scores[player]
            rank = 1
            for other_player, other_score in scores.items():
                if other_score > player_score:
                    rank += 1
            print(f"{player} is rank {rank}")
            
        elif command == "top":
            n = int(parts[1])
            sorted_players = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            for i in range(min(n, len(sorted_players))):
                player, score = sorted_players[i]
                print(f"{i + 1}. {player}: {score}")

if __name__ == "__main__":
    main()