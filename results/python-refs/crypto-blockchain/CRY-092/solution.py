# Read input
total_tokens = int(input())
cliff_months = int(input())
vesting_months = int(input())
start_timestamp = int(input())
query_timestamp = int(input())

# Calculate elapsed time in seconds
elapsed_seconds = query_timestamp - start_timestamp

# Convert to months (using average month length)
seconds_per_month = 30.44 * 24 * 3600  # Average days per month
elapsed_months = elapsed_seconds / seconds_per_month

# Calculate vested amount
if elapsed_months < cliff_months:
    vested_amount = 0
else:
    # Linear vesting after cliff
    vesting_progress = min(1.0, elapsed_months / vesting_months)
    vested_amount = int(total_tokens * vesting_progress)

unvested_amount = total_tokens - vested_amount

print(vested_amount)
print(unvested_amount)