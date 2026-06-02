import math

initial_price = float(input())
current_price = float(input())

# Calculate price ratio
ratio = current_price / initial_price

# Impermanent loss formula for 50/50 LP
# IL = 2 * sqrt(ratio) / (1 + ratio) - 1
impermanent_loss = 2 * math.sqrt(ratio) / (1 + ratio) - 1

# Convert to percentage and format to 2 decimal places
il_percentage = abs(impermanent_loss) * 100
print(f"{il_percentage:.2f}")