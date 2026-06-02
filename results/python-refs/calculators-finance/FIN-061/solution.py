import sys

# Read total income
income = float(input().strip())

# Dictionary to store envelope data
envelopes = {}

# Read envelope allocations
while True:
    try:
        line = input().strip()
        if line.startswith('SPEND'):
            # Process spending
            parts = line.split()
            envelope_name = parts[1]
            amount = float(parts[2])
            if envelope_name in envelopes:
                envelopes[envelope_name]['spent'] += amount
        else:
            # Process envelope allocation
            parts = line.split()
            envelope_name = parts[0]
            percentage = float(parts[1])
            allocated = income * percentage / 100
            envelopes[envelope_name] = {
                'allocated': allocated,
                'spent': 0.0
            }
    except EOFError:
        break

# Output results
for envelope_name, data in envelopes.items():
    allocated = data['allocated']
    spent = data['spent']
    remaining = allocated - spent
    print(f"{envelope_name} {allocated:.2f} {spent:.2f} {remaining:.2f}")