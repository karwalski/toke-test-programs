import sys

# Read input
principal = float(input().strip())
annual_rate = float(input().strip())
compounds_per_year = int(input().strip())
years = int(input().strip())

# Calculate compound interest
# A = P(1 + r/n)^(nt)
final_amount = principal * (1 + annual_rate / compounds_per_year) ** (compounds_per_year * years)

# Output with 2 decimal places
print(f"{final_amount:.2f}")