import json
import sys

# Read input
n = int(input().strip())
json_data = input().strip()

# Parse JSON data
players = json.loads(json_data)

# Sort players by score in descending order
players.sort(key=lambda x: x['score'], reverse=True)

# Define ordinal suffixes
ordinals = ['1st', '2nd', '3rd']

# Output top N players
for i in range(min(n, len(players))):
    player = players[i]
    if i < 3:
        prefix = ordinals[i]
    else:
        prefix = f"{i+1}th"
    
    print(f"{prefix}: {player['player']} ({player['score']} pts)")