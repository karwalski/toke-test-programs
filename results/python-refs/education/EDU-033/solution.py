import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse JSON
flashcards = json.loads(input_data)

# Process each flashcard
for card in flashcards:
    front = card["front"]
    back = card["back"]
    tags = " ".join(card["tags"])
    
    # Output tab-separated format
    print(f"{front}\t{back}\t{tags}")