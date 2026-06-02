import sys

# Read input from stdin
line = input().strip()
cost, salvage_value, useful_life_years = map(int, line.split())

# Calculate annual depreciation using straight-line method
annual_depreciation = (cost - salvage_value) / useful_life_years

# Calculate and output depreciation schedule
book_value = cost
for year in range(1, useful_life_years + 1):
    book_value -= annual_depreciation
    print(f"{year},{annual_depreciation:.2f},{book_value:.2f}")