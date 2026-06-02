import json
import sys

# Read input
utxos_line = input().strip()
recipient = input().strip()
amount = float(input().strip())
fee = float(input().strip())

# Parse UTXOs
utxos = json.loads(utxos_line)

# Sort UTXOs by amount descending to try larger ones first
utxos.sort(key=lambda x: x['amount'], reverse=True)

# Select UTXOs using greedy algorithm
selected_utxos = []
total_input = 0
needed = amount + fee

for utxo in utxos:
    if total_input >= needed:
        break
    selected_utxos.append(utxo)
    total_input += utxo['amount']

# Build transaction
inputs = []
for utxo in selected_utxos:
    inputs.append({"txid": utxo["txid"], "vout": utxo["vout"]})

outputs = []
# Add recipient output
outputs.append({"address": recipient, "amount": amount})

# Calculate change
change = total_input - amount - fee
if change > 0:
    outputs.append({"address": "change", "amount": change})

# Build transaction object
transaction = {
    "inputs": inputs,
    "outputs": outputs
}

# Output JSON without spaces after separators
print(json.dumps(transaction, separators=(',', ':')))