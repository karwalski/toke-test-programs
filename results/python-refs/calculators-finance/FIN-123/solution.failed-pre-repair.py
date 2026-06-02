def calculate_moving_average(prices, period, index):
    if index < period - 1:
        return None
    return sum(prices[index - period + 1:index + 1]) / period

def detect_crosses(prices, short_period, long_period):
    crosses = []
    prev_short_ma = None
    prev_long_ma = None
    
    for i in range(len(prices)):
        short_ma = calculate_moving_average(prices, short_period, i)
        long_ma = calculate_moving_average(prices, long_period, i)
        
        if short_ma is not None and long_ma is not None and prev_short_ma is not None and prev_long_ma is not None:
            # Check for golden cross (short MA crosses above long MA)
            if prev_short_ma <= prev_long_ma and short_ma > long_ma:
                crosses.append((i, "GOLDEN_CROSS"))
            # Check for death cross (short MA crosses below long MA)
            elif prev_short_ma >= prev_long_ma and short_ma < long_ma:
                crosses.append((i, "DEATH_CROSS"))
        
        prev_short_ma = short_ma
        prev_long_ma = long_ma
    
    return crosses

# Read input
periods_line = input().strip()
short_period, long_period = map(int, periods_line.split())

prices_line = input().strip()
prices = list(map(float, prices_line.split(',')))

# Detect crosses
crosses = detect_crosses(prices, short_period, long_period)

# Output results
for index, cross_type in crosses:
    print(f"{index} {cross_type}")