import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse JSON
chains = json.loads(input_data)

# Find the winning chain
# Priority: highest cumulative_work, then highest length as tiebreaker
winning_chain = max(chains, key=lambda x: (x['cumulative_work'], x['length']))

# Output the chain_id
print(winning_chain['chain_id'])