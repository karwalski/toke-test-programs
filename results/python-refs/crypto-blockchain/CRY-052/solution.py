import json
import sys

# Read input
utxos_json = input().strip()
target_address = input().strip()

# Parse JSON
utxos = json.loads(utxos_json)

# Calculate total balance for target address
total_balance = 0.0
for utxo in utxos:
    if utxo["address"] == target_address:
        total_balance += utxo["amount"]

# Output the result
print(total_balance)