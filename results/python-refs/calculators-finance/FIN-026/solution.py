import sys

# Read input from stdin
line = input().strip()
cost, rate, years = line.split()
cost = float(cost)
rate = float(rate)
years = int(years)

# Calculate depreciation schedule
book_value = cost
for year in range(1, years + 1):
    depreciation = book_value * rate
    book_value = book_value - depreciation
    print(f"{year},{depreciation:.2f},{book_value:.2f}")