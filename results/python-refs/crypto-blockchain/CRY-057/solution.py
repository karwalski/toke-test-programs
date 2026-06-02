import sys
import json

nft_ownership = {}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    command = parts[0]
    
    if command == "MINT":
        token_id = parts[1]
        owner = parts[2]
        nft_ownership[token_id] = owner
    elif command == "TRANSFER":
        token_id = parts[1]
        from_owner = parts[2]
        to_owner = parts[3]
        if token_id in nft_ownership and nft_ownership[token_id] == from_owner:
            nft_ownership[token_id] = to_owner

# Sort by token_id and output as JSON
sorted_ownership = dict(sorted(nft_ownership.items(), key=lambda x: int(x[0])))
print(json.dumps(sorted_ownership, separators=(',', ':')))