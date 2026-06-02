import sys
import json

# Read input
target_address = input().strip()
transactions_json = input().strip()

# Parse JSON
transactions = json.loads(transactions_json)

# Calculate balance
balance = 0.0

for tx in transactions:
    if tx["to"] == target_address:
        # Receiving money
        balance += tx["amount"]
    elif tx["from"] == target_address:
        # Sending money (subtract amount and fee)
        balance -= tx["amount"]
        balance -= tx["fee"]

# Output the final balance
print(balance)