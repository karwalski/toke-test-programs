import json
import sys

# Read input
line1 = input().strip()
line2 = input().strip()

# Parse JSON transactions
transactions = json.loads(line1)
target_address = line2

# Calculate balance and next nonce
balance = 0
max_nonce = -1

for tx in transactions:
    if tx["from"] == target_address:
        balance -= tx["amount"]
        max_nonce = max(max_nonce, tx["nonce"])
    if tx["to"] == target_address:
        balance += tx["amount"]

next_nonce = max_nonce + 1

# Output
print(balance)
print(next_nonce)