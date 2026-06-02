import json
import sys
from collections import defaultdict

# Read input from stdin
input_data = sys.stdin.read().strip()
words = json.loads(input_data)

# Group words by difficulty tier
tiers = defaultdict(list)
for word_obj in words:
    tiers[word_obj['difficulty']].append(word_obj)

# Sort tiers by difficulty number and words within each tier alphabetically
for tier in sorted(tiers.keys()):
    print(f"--- Tier {tier} ---")
    sorted_words = sorted(tiers[tier], key=lambda x: x['word'])
    for word_obj in sorted_words:
        print(f"{word_obj['word']}: {word_obj['definition']}")