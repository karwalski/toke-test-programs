import json
import sys

# Read initial balances
initial_line = input().strip()
balances = json.loads(initial_line)

# Process transfer commands
for line in sys.stdin:
    line = line.strip()
    if line.startswith("TRANSFER"):
        parts = line.split()
        from_addr = parts[1]
        to_addr = parts[2]
        amount = int(parts[3])
        
        balances[from_addr] -= amount
        balances[to_addr] += amount

# Sort by address and output
sorted_balances = dict(sorted(balances.items()))
print(json.dumps(sorted_balances, separators=(',', ':')))