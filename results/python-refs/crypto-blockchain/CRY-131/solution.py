total_staked = float(input())
daily_reward = float(input())
token_price = float(input())
staked_token_price = float(input())

daily_reward_value = daily_reward * token_price
total_staked_value = total_staked * staked_token_price
daily_yield = daily_reward_value / total_staked_value
apy = daily_yield * 365 * 100

print(f"{apy:.2f}")