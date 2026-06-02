import sys

# Read input from stdin
input_line = sys.stdin.read().strip()
values = list(map(float, input_line.split(',')))

# Calculate time-weighted return
# Time-weighted return = (V_final / V_initial) - 1
initial_value = values[0]
final_value = values[-1]

# Total return
total_return = (final_value / initial_value) - 1

# Annualized return (assuming monthly periods)
# Number of periods = number of values - 1 (since first is initial)
num_periods = len(values) - 1
# Annualized return = ((1 + total_return) ^ (12/num_periods)) - 1
annualized_return = ((1 + total_return) ** (12 / num_periods)) - 1

# Format to percentage with 2 decimal places
total_return_pct = total_return * 100
annualized_return_pct = annualized_return * 100

# Output
print(f"{total_return_pct:.2f}%")
print(f"{annualized_return_pct:.2f}%")