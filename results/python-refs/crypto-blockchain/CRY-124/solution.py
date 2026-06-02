import json
import sys

# Read the first line containing confirmed nonces
confirmed_line = input().strip()
confirmed_nonces = json.loads(confirmed_line)

# Track pending transactions for each address
pending_counts = {}

# Process remaining lines
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    command = parts[0]
    address = parts[1]
    
    if command == "PENDING":
        # Track pending transaction for this address
        if address not in pending_counts:
            pending_counts[address] = 0
        pending_counts[address] += 1
    
    elif command == "NEXT":
        # Calculate next available nonce
        last_confirmed = confirmed_nonces.get(address, -1)
        pending_count = pending_counts.get(address, 0)
        next_nonce = last_confirmed + 1 + pending_count
        print(next_nonce)