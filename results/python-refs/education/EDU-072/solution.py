import sys
import json
from datetime import datetime

# Read input
date_str = input().strip()
vocab_json = input().strip()

# Parse the vocabulary list
vocab_list = json.loads(vocab_json)

# Parse the date and use it to select a word
date_obj = datetime.fromisoformat(date_str)
# Use day of year as index to make selection deterministic based on date
day_of_year = date_obj.timetuple().tm_yday
selected_word = vocab_list[(day_of_year - 1) % len(vocab_list)]

# Output the formatted word-of-the-day block
print(f"Word of the Day: {selected_word['word']}")
print(f"Definition: {selected_word['definition']}")
print(f"Example: {selected_word['example']}")