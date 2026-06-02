import json
import sys
from datetime import datetime

# Read input
today_str = input().strip()
cards_json = input().strip()

# Parse input
today = datetime.strptime(today_str, "%Y-%m-%d").date()
cards = json.loads(cards_json)

# Categorize cards
overdue = []
due_today = []
upcoming = []

for card in cards:
    due_date = datetime.strptime(card["due_date"], "%Y-%m-%d").date()
    
    if due_date < today:
        overdue.append(card)
    elif due_date == today:
        due_today.append(card)
    else:
        upcoming.append(card)

# Sort overdue by priority (higher priority first)
overdue.sort(key=lambda x: x["priority"], reverse=True)

# Output results
if overdue:
    for card in overdue:
        print(f"OVERDUE: {card['id']} - {card['topic']} (was due {card['due_date']})")

if due_today:
    for card in due_today:
        print(f"DUE TODAY: {card['id']} - {card['topic']}")

if upcoming:
    for card in upcoming:
        print(f"UPCOMING: {card['id']} - {card['topic']} (due {card['due_date']})")