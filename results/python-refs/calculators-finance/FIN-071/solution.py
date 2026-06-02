import sys

# Read all input lines
lines = []
for line in sys.stdin:
    line = line.strip()
    if line:
        lines.append(line)

# Parse and store accounts
accounts = []
total_dr = 0
total_cr = 0

for line in lines:
    parts = line.rsplit(' ', 2)  # Split from right to get last 2 parts
    account = parts[0]
    amount = int(parts[1])
    dr_cr = parts[2]
    
    accounts.append((account, amount, dr_cr))
    
    if dr_cr == 'DR':
        total_dr += amount
    else:  # CR
        total_cr += amount

# Output the trial balance
for account, amount, dr_cr in accounts:
    print(f"{account} {amount} {dr_cr}")

print(f"TOTAL DR: {total_dr} CR: {total_cr}")

# Check if balanced
if total_dr == total_cr:
    print("BALANCED")
else:
    diff = abs(total_dr - total_cr)
    print(f"UNBALANCED {diff}")