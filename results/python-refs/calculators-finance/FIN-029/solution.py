import sys

# Read the first line with amount and currencies
first_line = input().strip().split()
amount = float(first_line[0])
source_currency = first_line[1]
target_currency = first_line[2]

# Read exchange rates
exchange_rates = {}
try:
    while True:
        line = input().strip()
        if line:
            parts = line.split()
            cur1, cur2, rate = parts[0], parts[1], float(parts[2])
            exchange_rates[(cur1, cur2)] = rate
except EOFError:
    pass

# Convert currency
if (source_currency, target_currency) in exchange_rates:
    converted_amount = amount * exchange_rates[(source_currency, target_currency)]
elif (target_currency, source_currency) in exchange_rates:
    converted_amount = amount / exchange_rates[(target_currency, source_currency)]
else:
    # If no direct rate found, assume 1:1 (though this shouldn't happen in valid input)
    converted_amount = amount

# Output with exactly 2 decimal places
print(f"{converted_amount:.2f}")