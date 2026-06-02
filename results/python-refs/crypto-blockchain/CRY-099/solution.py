import sys
import math

# Read input
reserve_in = int(input().strip())
reserve_out = int(input().strip())
amount_in = int(input().strip())
fee_percent = float(input().strip())

# Calculate amount out using constant product formula with fee
# Formula: amount_out = (reserve_out * amount_in_after_fee) / (reserve_in + amount_in_after_fee)
# where amount_in_after_fee = amount_in * (1 - fee_percent / 100)

amount_in_after_fee = amount_in * (1 - fee_percent / 100)
amount_out = (reserve_out * amount_in_after_fee) / (reserve_in + amount_in_after_fee)

# Floor the result and convert to integer
result = int(math.floor(amount_out))

print(result)