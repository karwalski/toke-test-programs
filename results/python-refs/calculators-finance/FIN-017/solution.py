import math

# Read input
line = input().strip()
values = line.split()
stock_price = float(values[0])
strike_price = float(values[1])
time_years = float(values[2])
risk_free_rate = float(values[3])
volatility = float(values[4])

# Calculate d1 and d2
d1 = (math.log(stock_price / strike_price) + (risk_free_rate + 0.5 * volatility**2) * time_years) / (volatility * math.sqrt(time_years))
d2 = d1 - volatility * math.sqrt(time_years)

# Calculate cumulative standard normal distribution
def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

# Calculate call option price using Black-Scholes formula
call_price = stock_price * norm_cdf(d1) - strike_price * math.exp(-risk_free_rate * time_years) * norm_cdf(d2)

# Output result to 4 decimal places
print(f"{call_price:.4f}")